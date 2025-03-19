-- Création de la base de données
CREATE DATABASE IF NOT EXISTS bibliotheque;
USE bibliotheque;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    date_inscription DATE NOT NULL,
    est_administrateur BOOLEAN DEFAULT FALSE,
    est_actif BOOLEAN DEFAULT TRUE,
    telephone VARCHAR(15),
    adresse TEXT
);

-- Table des catégories de livres
CREATE TABLE IF NOT EXISTS categories (
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Table des auteurs
CREATE TABLE IF NOT EXISTS auteurs (
    id_auteur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    date_naissance DATE,
    bio TEXT
);

-- Table des livres
CREATE TABLE IF NOT EXISTS livres (
    id_livre INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    annee_publication INT,
    editeur VARCHAR(100),
    resume TEXT,
    langue VARCHAR(30),
    nombre_pages INT,
    id_categorie INT,
    date_ajout DATE NOT NULL,
    FOREIGN KEY (id_categorie) REFERENCES categories(id_categorie) ON DELETE SET NULL
);

-- Table de liaison entre livres et auteurs (relation many-to-many)
CREATE TABLE IF NOT EXISTS livre_auteur (
    id_livre INT,
    id_auteur INT,
    PRIMARY KEY (id_livre, id_auteur),
    FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE,
    FOREIGN KEY (id_auteur) REFERENCES auteurs(id_auteur) ON DELETE CASCADE
);

-- Table des exemplaires physiques de livres
CREATE TABLE IF NOT EXISTS exemplaires (
    id_exemplaire INT AUTO_INCREMENT PRIMARY KEY,
    id_livre INT NOT NULL,
    code_reference VARCHAR(50) UNIQUE NOT NULL,
    etat VARCHAR(20) NOT NULL,
    date_acquisition DATE NOT NULL,
    est_disponible BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
);

-- Table des emprunts
CREATE TABLE IF NOT EXISTS emprunts (
    id_emprunt INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_exemplaire INT NOT NULL,
    date_emprunt DATE NOT NULL,
    date_retour_prevue DATE NOT NULL,
    date_retour_effective DATE,
    est_retourne BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_exemplaire) REFERENCES exemplaires(id_exemplaire) ON DELETE CASCADE
);

-- Table des réservations
CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    date_reservation DATE NOT NULL,
    est_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
);

-- Table des notifications
CREATE TABLE IF NOT EXISTS notifications (
    id_notification INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    message TEXT NOT NULL,
    date_creation DATETIME NOT NULL,
    est_lue BOOLEAN DEFAULT FALSE,
    type_notification VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE
);

-- Table des avis sur les livres
CREATE TABLE IF NOT EXISTS avis (
    id_avis INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT NOT NULL,
    id_livre INT NOT NULL,
    note INT NOT NULL CHECK (note BETWEEN 1 AND 5),
    commentaire TEXT,
    date_avis DATE NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE,
    FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
);

-- Table des statistiques d'utilisation
CREATE TABLE IF NOT EXISTS statistiques (
    id_statistique INT AUTO_INCREMENT PRIMARY KEY,
    id_livre INT NOT NULL,
    nombre_emprunts INT DEFAULT 0,
    nombre_reservations INT DEFAULT 0,
    note_moyenne FLOAT DEFAULT 0,
    derniere_mise_a_jour DATETIME NOT NULL,
    FOREIGN KEY (id_livre) REFERENCES livres(id_livre) ON DELETE CASCADE
);

-- Créer des index pour optimiser les recherches
CREATE INDEX idx_livre_titre ON livres(titre);
CREATE INDEX idx_emprunt_dates ON emprunts(date_emprunt, date_retour_prevue);
CREATE INDEX idx_livre_categorie ON livres(id_categorie);
CREATE INDEX idx_exemplaire_disponibilite ON exemplaires(est_disponible);