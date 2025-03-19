import sqlite3
import datetime
import hashlib
import os

DB_PATH = 'bibliotheque.db'

def init_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    
    # Création de toutes les tables en premier
    create_tables(cur)
    
    # Vérification des tables créées
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("Tables créées:", cur.fetchall())
    
    # Insertion des données
    add_default_admin(cur)
    add_default_categories(cur)
    add_example_books(cur)
    
    conn.commit()
    conn.close()
    print("Base initialisée avec succès")

def create_tables(cur):
    """Version corrigée avec ordre de création strict"""
    # 1. Table utilisateurs (sans dépendances)
    cur.execute('''
        CREATE TABLE utilisateurs (
            id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL,
            date_inscription TEXT NOT NULL,
            est_administrateur INTEGER DEFAULT 0,
            est_actif INTEGER DEFAULT 1,
            telephone TEXT,
            adresse TEXT
        )
    ''')
    
    # 2. Catégories (sans dépendances)
    cur.execute('''
        CREATE TABLE categories (
            id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_categorie TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # 3. Auteurs (sans dépendances)
    cur.execute('''
        CREATE TABLE auteurs (
            id_auteur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            bio TEXT
        )
    ''')
    
    # 4. Livres (dépend de catégories)
    cur.execute('''
        CREATE TABLE livres (
            id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            isbn TEXT UNIQUE,
            annee_publication INTEGER,
            editeur TEXT,
            resume TEXT,
            langue TEXT,
            nombre_pages INTEGER,
            id_categorie INTEGER,
            date_ajout TEXT NOT NULL,
            FOREIGN KEY (id_categorie) REFERENCES categories(id_categorie)
        )
    ''')
    
    # 5. Livre-Auteur (dépend de livres et auteurs)
    cur.execute('''
        CREATE TABLE livre_auteur (
            id_livre INTEGER,
            id_auteur INTEGER,
            PRIMARY KEY (id_livre, id_auteur),
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre),
            FOREIGN KEY (id_auteur) REFERENCES auteurs(id_auteur)
        )
    ''')
    
    # 6. Exemplaires (dépend de livres)
    cur.execute('''
        CREATE TABLE exemplaires (
            id_exemplaire INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            code_reference TEXT UNIQUE NOT NULL,
            etat TEXT NOT NULL,
            date_acquisition TEXT NOT NULL,
            est_disponible INTEGER DEFAULT 1,
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre)
        )
    ''')
    
    # ... (autres tables conservent leur ordre actuel)

# Les autres fonctions (hash_password, add_default_admin, etc.) restent identiques

if __name__ == "__main__":
    init_database()