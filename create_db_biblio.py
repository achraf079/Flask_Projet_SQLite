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
    
    # Valider les changements et fermer
    conn.commit()
    conn.close()
    print(f"Base de données initialisée avec succès: {os.path.abspath(DB_PATH)}")

def create_tables(cur):
    """Création de toutes les tables en une seule transaction"""
    # Table des utilisateurs
    cur.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
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
    
    # Table des catégories
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_categorie TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Table des auteurs
    cur.execute('''
        CREATE TABLE IF NOT EXISTS auteurs (
            id_auteur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_naissance TEXT,
            bio TEXT
        )
    ''')
    
    # Table des livres (avant la table livre_auteur qui y fait référence)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS livres (
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
    
    # Table de liaison entre livres et auteurs
    cur.execute('''
        CREATE TABLE IF NOT EXISTS livre_auteur (
            id_livre INTEGER,
            id_auteur INTEGER,
            PRIMARY KEY (id_livre, id_auteur),
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE,
            FOREIGN KEY (id_auteur) REFERENCES auteurs(id_auteur) ON DELETE CASCADE
        )
    ''')
    
    # Table des exemplaires
    cur.execute('''
        CREATE TABLE IF NOT EXISTS exemplaires (
            id_exemplaire INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            code_reference TEXT UNIQUE NOT NULL,
            etat TEXT NOT NULL,
            date_acquisition TEXT NOT NULL,
            est_disponible INTEGER DEFAULT 1,
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
        )
    ''')
    
    # Table des emprunts
    cur.execute('''
        CREATE TABLE IF NOT EXISTS emprunts (
            id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL,
            id_exemplaire INTEGER NOT NULL,
            date_emprunt TEXT NOT NULL,
            date_retour_prevue TEXT NOT NULL,
            date_retour_effective TEXT,
            est_retourne INTEGER DEFAULT 0,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
            FOREIGN KEY (id_exemplaire) REFERENCES exemplaires(id_exemplaire) ON DELETE CASCADE
        )
    ''')
    
    # Table des réservations
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL,
            id_livre INTEGER NOT NULL,
            date_reservation TEXT NOT NULL,
            est_active INTEGER DEFAULT 1,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
        )
    ''')
    
    # Table des notifications
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL,
            message TEXT NOT NULL,
            date_creation TEXT NOT NULL,
            est_lue INTEGER DEFAULT 0,
            type_notification TEXT NOT NULL,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE
        )
    ''')
    
    # Table des avis
    cur.execute('''
        CREATE TABLE IF NOT EXISTS avis (
            id_avis INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL,
            id_livre INTEGER NOT NULL,
            note INTEGER NOT NULL CHECK (note BETWEEN 1 AND 5),
            commentaire TEXT,
            date_avis TEXT NOT NULL,
            FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
        )
    ''')
    
    # Table des statistiques
    cur.execute('''
        CREATE TABLE IF NOT EXISTS statistiques (
            id_statistique INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            nombre_emprunts INTEGER DEFAULT 0,
            nombre_reservations INTEGER DEFAULT 0,
            note_moyenne REAL DEFAULT 0,
            derniere_mise_a_jour TEXT NOT NULL,
            FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
        )
    ''')
    
    # Créer des index pour optimiser les recherches
    cur.execute("CREATE INDEX IF NOT EXISTS idx_livre_titre ON livres(titre)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_emprunt_dates ON emprunts(date_emprunt, date_retour_prevue)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_livre_categorie ON livres(id_categorie)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_exemplaire_disponibilite ON exemplaires(est_disponible)")
    
    print("Toutes les tables ont été créées avec succès.")

def hash_password(password):
    """Création d'un hash de mot de passe sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_default_admin(cur):
    """Ajout d'un utilisateur administrateur par défaut"""
    # Date d'aujourd'hui au format ISO
    today = datetime.date.today().isoformat()
    # Mot de passe hashé
    hashed_password = hash_password("admin123")
    
    # Insertion directe sans vérification (puisque nous recréons la BD)
    cur.execute('''
        INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, date_inscription, est_administrateur)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("Admin", "Système", "admin@bibliotheque.fr", hashed_password, today, 1))
    
    print("Administrateur par défaut créé avec succès.")

def add_default_categories(cur):
    """Ajout des catégories par défaut"""
    categories = [
        ("Roman", "Livres de fiction narrative"),
        ("Science-Fiction", "Œuvres d'anticipation et de mondes futuristes"),
        ("Policier", "Romans d'enquête et de mystère"),
        ("Biographie", "Récits de vie de personnalités"),
        ("Histoire", "Ouvrages historiques et documentaires"),
        ("Philosophie", "Ouvrages de réflexion et de pensée"),
        ("Sciences", "Ouvrages scientifiques et techniques"),
        ("Jeunesse", "Livres pour enfants et adolescents")
    ]
    
    for nom, description in categories:
        cur.execute('''
            INSERT INTO categories (nom_categorie, description)
            VALUES (?, ?)
        ''', (nom, description))
    
    print("Catégories par défaut ajoutées avec succès.")

if __name__ == "__main__":
    print("Initialisation de la base de données SQLite de la bibliothèque...")
    init_database()