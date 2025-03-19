import sqlite3
import os
from datetime import datetime, timedelta

# Fonction pour initialiser la base de données
def init_database():
    # Supprimer la base de données existante si elle existe
    if os.path.exists('database.db'):
        os.remove('database.db')
    
    # Créer une connexion à la base de données
    connection = sqlite3.connect('database.db')
    
    # Exécuter le script SQL depuis le fichier schema.sql
    with open('schema.sql') as f:
        connection.executescript(f.read())
    
    # Créer un curseur
    cur = connection.cursor()
    
    # Insérer les clients (reprend votre code existant)
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('DUPONT', 'Emilie', '123, Rue des Lilas, 75001 Paris'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('LEROUX', 'Lucas', '456, Avenue du Soleil, 31000 Toulouse'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('MARTIN', 'Amandine', '789, Rue des Érables, 69002 Lyon'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('TREMBLAY', 'Antoine', '1010, Boulevard de la Mer, 13008 Marseille'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('LAMBERT', 'Sarah', '222, Avenue de la Liberté, 59000 Lille'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('GAGNON', 'Nicolas', '456, Boulevard des Cerisiers, 69003 Lyon'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('DUBOIS', 'Charlotte', '789, Rue des Roses, 13005 Marseille'))
    cur.execute("INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)",
                ('LEFEVRE', 'Thomas', '333, Rue de la Paix, 75002 Paris'))
    

    
    # Ajouter quelques avis
    cur.execute("""
        INSERT INTO avis (id_livre, id_client, note, commentaire) 
        VALUES (?, ?, ?, ?)
    """, (1, 2, 4.5, "Un classique intemporel qui reste terriblement actuel."))
    
    cur.execute("""
        INSERT INTO avis (id_livre, id_client, note, commentaire) 
        VALUES (?, ?, ?, ?)
    """, (2, 3, 5.0, "Un livre magnifique, à la fois simple et profond."))
    
    # Ajouter quelques notifications
    cur.execute("""
        INSERT INTO notification (id_client, id_emprunt, type, message) 
        VALUES (?, ?, ?, ?)
    """, (3, 3, 'retard', "Votre livre 'Le Petit Prince' est en retard. Merci de le retourner rapidement."))
    
    # Valider les changements et fermer la connexion
    connection.commit()
    connection.close()
    
    print("Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_database()