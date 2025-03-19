import sqlite3
import datetime
import hashlib
import os

DB_PATH = 'bibliotheque.db'

def init_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Ancienne base de données supprimée.")
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    
    # 1. Création de TOUTES les tables en premier
    create_tables(cur)
    
    # 2. Insertion des données APRÈS la création des tables
    add_default_admin(cur)
    add_default_categories(cur)
    add_example_books(cur)
    
    conn.commit()
    conn.close()
    print(f"Base initialisée : {os.path.abspath(DB_PATH)}")

def create_tables(cur):
    """Version complète et correcte de la création des tables"""
    # Table utilisateurs
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
    
    # Table catégories
    cur.execute('''
        CREATE TABLE categories (
            id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_categorie TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Table auteurs (CRÉÉE AVANT les livres)
    cur.execute('''
        CREATE TABLE auteurs (
            id_auteur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            bio TEXT
        )
    ''')
    
    # Table livres
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
            FOREIGN KEY (id_categorie) REFERENCES categories(id_categorie) ON DELETE SET NULL
        )
    ''')
    
    # Table de liaison livre_auteur (CRÉÉE APRÈS livres et auteurs)
    cur.execute('''
        CREATE TABLE livre_auteur (
            id_livre INTEGER,
            id_auteur INTEGER,
            PRIMARY KEY (id_livre, id_auteur),
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE,
            FOREIGN KEY (id_auteur) REFERENCES auteurs(id_auteur) ON DELETE CASCADE
        )
    ''')
    
    # Reste des tables (exemplaires, emprunts, etc.)
    # ... [le code existant pour les autres tables] ...

    print("Toutes les tables créées avec succès.")

# ... [les autres fonctions restent identiques] ...

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    init_database()