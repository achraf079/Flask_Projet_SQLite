-- Création des tables pour la bibliothèque
PRAGMA foreign_keys = ON;

-- Table des clients (déjà existante dans votre script)
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    adresse TEXT,
    email TEXT,
    telephone TEXT,
    date_inscription TEXT DEFAULT CURRENT_DATE,
    role TEXT DEFAULT 'membre'
);

-- Table CATEGORIE
CREATE TABLE IF NOT EXISTS categorie (
    id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_categorie TEXT NOT NULL,
    description TEXT
);

-- Table LIVRE
CREATE TABLE IF NOT EXISTS livre (
    id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    isbn TEXT UNIQUE,
    resume TEXT,
    annee_publication INTEGER,
    editeur TEXT,
    langue TEXT DEFAULT 'Français',
    nb_pages INTEGER,
    couverture_url TEXT,
    id_categorie INTEGER,
    FOREIGN KEY (id_categorie) REFERENCES categorie(id_categorie)
);

-- Table EXEMPLAIRE
CREATE TABLE IF NOT EXISTS exemplaire (
    id_exemplaire INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    cote TEXT NOT NULL,
    etat TEXT CHECK(etat IN ('neuf', 'bon', 'moyen', 'abîmé', 'inutilisable')) DEFAULT 'bon',
    disponible INTEGER DEFAULT 1,
    date_acquisition TEXT NOT NULL,
    prix_acquisition REAL,
    notes TEXT,
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre)
);

-- Table EMPRUNT
CREATE TABLE IF NOT EXISTS emprunt (
    id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
    id_exemplaire INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    date_emprunt TEXT NOT NULL DEFAULT CURRENT_DATE,
    date_retour_prevue TEXT NOT NULL,
    date_retour_effective TEXT,
    statut TEXT CHECK(statut IN ('en_cours', 'retourné', 'en_retard', 'perdu')) DEFAULT 'en_cours',
    notes TEXT,
    FOREIGN KEY (id_exemplaire) REFERENCES exemplaire(id_exemplaire),
    FOREIGN KEY (id_client) REFERENCES clients(id)
);

-- Table RESERVATION
CREATE TABLE IF NOT EXISTS reservation (
    id_reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    date_reservation TEXT NOT NULL DEFAULT CURRENT_DATE,
    date_expiration TEXT NOT NULL,
    statut TEXT CHECK(statut IN ('en_attente', 'disponible', 'annulée', 'terminée')) DEFAULT 'en_attente',
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre),
    FOREIGN KEY (id_client) REFERENCES clients(id)
);

-- Table NOTIFICATION
CREATE TABLE IF NOT EXISTS notification (
    id_notification INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    id_emprunt INTEGER,
    type TEXT CHECK(type IN ('retard', 'reservation_disponible', 'rappel', 'information')) NOT NULL,
    message TEXT NOT NULL,
    date_envoi TEXT DEFAULT CURRENT_TIMESTAMP,
    lu INTEGER DEFAULT 0,
    FOREIGN KEY (id_client) REFERENCES clients(id),
    FOREIGN KEY (id_emprunt) REFERENCES emprunt(id_emprunt)
);

-- Table AVIS
CREATE TABLE IF NOT EXISTS avis (
    id_avis INTEGER PRIMARY KEY AUTOINCREMENT,
    id_livre INTEGER NOT NULL,
    id_client INTEGER NOT NULL,
    note REAL CHECK (note >= 0 AND note <= 5),
    commentaire TEXT,
    date_avis TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_livre) REFERENCES livre(id_livre),
    FOREIGN KEY (id_client) REFERENCES clients(id),
    UNIQUE (id_livre, id_client)
);

-- Table HISTORIQUE_ACTIONS
CREATE TABLE IF NOT EXISTS historique_actions (
    id_action INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER,
    action TEXT NOT NULL,
    entite TEXT NOT NULL,
    id_entite INTEGER NOT NULL,
    details TEXT,
    date_action TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_client) REFERENCES clients(id)
);

-- Insérer quelques catégories de base
INSERT INTO categorie (nom_categorie, description) VALUES
('Roman', 'Œuvres de fiction narrative en prose'),
('Science-Fiction', 'Romans et nouvelles basés sur des progrès scientifiques et technologiques futurs'),
('Policier', 'Romans centrés sur la résolution d''une enquête policière'),
('Biographie', 'Récits de vie d''une personne écrite par une autre personne'),
('Histoire', 'Livres sur des événements historiques réels'),
('Informatique', 'Livres techniques sur la programmation et l''informatique'),
('Philosophie', 'Ouvrages de réflexion sur l''existence, la connaissance et la morale'),
('Poésie', 'Recueils d''œuvres poétiques');

-- Insérer quelques livres
INSERT INTO livre (titre, auteur, isbn, resume, annee_publication, editeur, id_categorie) VALUES
('1984', 'George Orwell', '978-2070368228', 'Un roman dystopique sur un régime totalitaire', 1949, 'Gallimard', 2),
('Le Petit Prince', 'Antoine de Saint-Exupéry', '978-2070612758', 'Conte poétique et philosophique sous l''apparence d''un conte pour enfants', 1943, 'Gallimard', 1),
('Les Misérables', 'Victor Hugo', '978-2253096337', 'Fresque sociale et historique du XIXe siècle', 1862, 'Livre de Poche', 1),
('Apprendre Python', 'Mark Lutz', '978-2416005657', 'Guide complet pour apprendre la programmation en Python', 2019, 'O''Reilly', 6),
('L''Étranger', 'Albert Camus', '978-2070360024', 'Roman emblématique de l''absurde', 1942, 'Gallimard', 1),
('Sapiens: Une brève histoire de l''humanité', 'Yuval Noah Harari', '978-2226257017', 'Histoire de l''Homo Sapiens de la préhistoire au XXIe siècle', 2015, 'Albin Michel', 5);

-- Insérer quelques exemplaires
INSERT INTO exemplaire (id_livre, cote, etat, disponible, date_acquisition, prix_acquisition) VALUES
(1, 'ROM-ORW-01', 'bon', 1, '2022-01-15', 9.90),
(1, 'ROM-ORW-02', 'moyen', 1, '2022-01-15', 9.90),
(2, 'ROM-SAI-01', 'bon', 1, '2022-02-10', 7.50),
(3, 'ROM-HUG-01', 'bon', 1, '2022-03-05', 12.90),
(3, 'ROM-HUG-02', 'neuf', 1, '2023-01-20', 12.90),
(4, 'INF-LUT-01', 'neuf', 1, '2023-02-15', 39.90),
(5, 'ROM-CAM-01', 'bon', 1, '2022-05-12', 6.90),
(6, 'HIS-HAR-01', 'bon', 1, '2022-06-22', 24.90);

-- Créer des index pour optimiser les recherches
CREATE INDEX IF NOT EXISTS idx_livre_titre ON livre(titre);
CREATE INDEX IF NOT EXISTS idx_livre_auteur ON livre(auteur);
CREATE INDEX IF NOT EXISTS idx_exemplaire_disponible ON exemplaire(disponible);
CREATE INDEX IF NOT EXISTS idx_emprunt_statut ON emprunt(statut);