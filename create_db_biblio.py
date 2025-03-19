import sqlite3
import datetime
import hashlib
import os

# Chemin de la base de données
DB_PATH = 'bibliotheque.db'

def init_database():
    # Si la base de données existe déjà, la supprimer pour tout recréer proprement
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Ancienne base de données supprimée.")
    
    # Créer une nouvelle connexion
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    
    # Créer toutes les tables d'abord
    create_tables(cur)
    
    # Puis ajouter les données initiales
    add_default_admin(cur)
    add_default_categories(cur)
    add_example_books(cur)  # Nouvelle fonction d'ajout de livres
    
    # Valider les changements et fermer
    conn.commit()
    conn.close()
    print(f"Base de données initialisée avec succès: {os.path.abspath(DB_PATH)}")

def create_tables(cur):
    """Création de toutes les tables en une seule transaction"""
    # ... (le code de création des tables reste identique) ...
    # (Les tables utilisateurs, categories, auteurs, livres, etc.)

def hash_password(password):
    """Création d'un hash de mot de passe sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_default_admin(cur):
    """Ajout d'un utilisateur administrateur par défaut"""
    # ... (le code existant reste inchangé) ...

def add_default_categories(cur):
    """Ajout des catégories par défaut"""
    # ... (le code existant reste inchangé) ...

def add_example_books(cur):
    """Ajout de livres exemples avec auteurs et exemplaires"""
    # Ajout des auteurs
    auteurs = [
        ("Hugo", "Victor", "1802-02-26", "Écrivain romantique français"),
        ("Orwell", "George", "1903-06-25", "Écrivain et journaliste anglais"),
        ("de Saint-Exupéry", "Antoine", "1900-06-29", "Écrivain et aviateur")
    ]
    
    auteurs_ids = {}
    for nom, prenom, naissance, bio in auteurs:
        cur.execute('''
            INSERT INTO auteurs (nom, prenom, date_naissance, bio)
            VALUES (?, ?, ?, ?)
        ''', (nom, prenom, naissance, bio))
        auteurs_ids[(prenom, nom)] = cur.lastrowid

    # Livres avec leurs métadonnées
    livres_data = [
        {
            "titre": "Les Misérables",
            "isbn": "978-2070409228",
            "annee": 1862,
            "editeur": "Éditions Gallimard",
            "resume": "Un roman historique qui explore la nature du bien et du mal à travers le parcours de Jean Valjean.",
            "langue": "Français",
            "pages": 1488,
            "categorie": 1,  # Roman
            "auteurs": [("Victor", "Hugo")],
            "exemplaires": 3
        },
        {
            "titre": "1984",
            "isbn": "978-2070368228",
            "annee": 1949,
            "editeur": "Gallimard",
            "resume": "Une dystopie célèbre sur la surveillance totale et le pouvoir totalitaire.",
            "langue": "Anglais",
            "pages": 328,
            "categorie": 2,  # Science-Fiction
            "auteurs": [("George", "Orwell")],
            "exemplaires": 2
        },
        {
            "titre": "Le Petit Prince",
            "isbn": "978-2070408504",
            "annee": 1943,
            "editeur": "Gallimard",
            "resume": "Conte philosophique poétique sur l'amitié et la nature humaine.",
            "langue": "Français",
            "pages": 96,
            "categorie": 8,  # Jeunesse
            "auteurs": [("Antoine", "de Saint-Exupéry")],
            "exemplaires": 5
        }
    ]

    for livre in livres_data:
        # Insertion du livre
        cur.execute('''
            INSERT INTO livres (
                titre, isbn, annee_publication, editeur, resume, 
                langue, nombre_pages, id_categorie, date_ajout
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            livre["titre"],
            livre["isbn"],
            livre["annee"],
            livre["editeur"],
            livre["resume"],
            livre["langue"],
            livre["pages"],
            livre["categorie"],
            datetime.date.today().isoformat()
        ))
        livre_id = cur.lastrowid

        # Liaison avec les auteurs
        for auteur in livre["auteurs"]:
            cur.execute('''
                INSERT INTO livre_auteur (id_livre, id_auteur)
                VALUES (?, ?)
            ''', (livre_id, auteurs_ids[auteur]))

        # Ajout des exemplaires
        for i in range(1, livre["exemplaires"] + 1):
            code_ref = f"{livre['titre'][:3].upper()}-{i:03d}"
            cur.execute('''
                INSERT INTO exemplaires (
                    id_livre, code_reference, etat, 
                    date_acquisition, est_disponible
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                livre_id,
                code_ref,
                "Neuf",
                datetime.date.today().isoformat(),
                1  # Disponible par défaut
            ))

    print("Livres exemples ajoutés avec succès.")

if __name__ == "__main__":
    print("Initialisation de la base de données SQLite de la bibliothèque...")
    init_database()