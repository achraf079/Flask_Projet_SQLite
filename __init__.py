from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session, flash
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import datetime
from datetime import timedelta


def get_db_connection():
    return sqlite3.connect('bibliotheque.db')


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur


def est_authentifie():
    return session.get('authentifie')


@app.route('/')
def index():
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;')
    data = cursor.fetchall()
    conn.close()
    return render_template('accueil.html', data=data)


@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"


@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        # password à cacher par la suite
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)


@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('bibliotheque.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('page_accueil.html', data=data)


@app.route('/categories/')
def afficher_categories():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_categorie, nom_categorie FROM categories")
    categories = cur.fetchall()
    conn.close()

    return render_template('categories.html', categories=categories)


@app.route('/ajout_livre', methods=['GET', 'POST'])
def ajout_livre():
    conn = get_db_connection()
    cur = conn.cursor()

    # Récupération des catégories existantes
    cur.execute("SELECT id_categorie, nom_categorie FROM categories")
    categories = cur.fetchall()

    if request.method == 'POST':
        # Récupération des données du formulaire
        titre = request.form.get('titre')
        auteur = request.form.get('auteur')
        isbn = request.form.get('isbn')
        editeur = request.form.get('editeur')
        annee_publication = request.form.get('annee')
        id_categorie = request.form.get('categorie')
        resume = request.form.get('description')
        nombre_exemplaires = request.form.get('stock')

        # Insertion du livre
        cur.execute('''
            INSERT INTO livres (titre, isbn, annee_publication, editeur, resume, langue, nombre_pages, id_categorie, date_ajout)  
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (titre, isbn, annee_publication, editeur, resume, 'Français', nombre_exemplaires, id_categorie, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()
        conn.close()

        flash('Le livre a été ajouté avec succès!')
        return redirect(url_for('ajout_livre'))  # Redirection après ajout

    return render_template('ajout_livre.html', categories=categories)


@app.route('/emprunt/ajouter', methods=['GET', 'POST'])
def ajout_emprunt():
    if request.method == 'POST':
        id_utilisateur = request.form['id_utilisateur']
        id_livre = request.form['id_livre']

        conn = get_db_connection()
        cur = conn.cursor()

        # Trouver un exemplaire disponible
        cur.execute(
            "SELECT id_exemplaire FROM exemplaires WHERE id_livre = ? AND est_disponible = 1 LIMIT 1", (id_livre,))
        exemplaire = cur.fetchone()

        if exemplaire:
            id_exemplaire = exemplaire['id_exemplaire']

            # Ajouter l'emprunt
            cur.execute('''
                INSERT INTO emprunts (id_utilisateur, id_exemplaire, date_emprunt, date_retour_prevue, est_retourne) 
                VALUES (?, ?, DATE('now'), DATE('now', '+14 days'), 0)
            ''', (id_utilisateur, id_exemplaire))

            # Mettre à jour la disponibilité de l'exemplaire
            cur.execute(
                "UPDATE exemplaires SET est_disponible = 0 WHERE id_exemplaire = ?", (id_exemplaire,))

            conn.commit()
            flash('Emprunt ajouté avec succès !')
        else:
            flash('Aucun exemplaire disponible pour ce livre.')

        conn.close()
        return redirect(url_for('liste_emprunts'))

    return render_template('ajout_emprunt.html')


# Route pour ajouter un nouveau lecteur
@app.route('/lecteur/ajouter', methods=['GET', 'POST'])
def ajout_lecteur():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO lecteurs (nom, prenom, email, telephone)
            VALUES (?, ?, ?, ?)
        ''', (nom, prenom, email, telephone))
        conn.commit()
        conn.close()

        flash('Le lecteur a été ajouté avec succès!')
        return redirect(url_for('ajouter_emprunt'))

    return render_template('ajout_lecteur.html')


@app.route('/init_db')
def init_db():
    conn = get_db_connection()

    # Créer les tables si elles n'existent pas
    conn.execute('''
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            isbn TEXT UNIQUE,
            editeur TEXT,
            annee INTEGER,
            categorie TEXT,
            description TEXT,
            stock INTEGER DEFAULT 1
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS lecteurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT,
            telephone TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livre_id INTEGER,
            lecteur_id INTEGER,
            date_emprunt DATE NOT NULL,
            date_retour_prevue DATE NOT NULL,
            date_retour DATE,
            FOREIGN KEY (livre_id) REFERENCES livres (id),
            FOREIGN KEY (lecteur_id) REFERENCES lecteurs (id)
        )
    ''')

    conn.commit()
    conn.close()

    flash('Base de données initialisée avec succès!')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
