# utils/db_setup.py - Configuration de la base de données

import sqlite3
import os

def setup_database():
    """Initialise la base de données si elle n'existe pas déjà"""
    db_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db')
    
    # Créer le répertoire de la base de données s'il n'existe pas
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_path = os.path.join(db_dir, 'database.db')
    
    # Se connecter à la base de données (la crée si elle n'existe pas)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Créer les tables si elles n'existent pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        description TEXT,
        categorie_id INTEGER,
        prix_achat REAL,
        prix_vente REAL,
        quantite INTEGER DEFAULT 0,
        seuil_reapprovisionnement INTEGER DEFAULT 5,
        FOREIGN KEY (categorie_id) REFERENCES categories (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fournisseurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        adresse TEXT,
        telephone TEXT,
        email TEXT,
        notes TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        adresse TEXT,
        telephone TEXT,
        email TEXT,
        notes TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS achats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fournisseur_id INTEGER,
        date_achat TEXT,
        montant_total REAL,
        notes TEXT,
        FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS details_achat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        achat_id INTEGER,
        produit_id INTEGER,
        quantite INTEGER,
        prix_unitaire REAL,
        FOREIGN KEY (achat_id) REFERENCES achats (id),
        FOREIGN KEY (produit_id) REFERENCES produits (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        date_vente TEXT,
        montant_total REAL,
        notes TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS details_vente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vente_id INTEGER,
        produit_id INTEGER,
        quantite INTEGER,
        prix_unitaire REAL,
        FOREIGN KEY (vente_id) REFERENCES ventes (id),
        FOREIGN KEY (produit_id) REFERENCES produits (id)
    )
    ''')
    
    # Insérer quelques catégories par défaut
    categories_default = [
        ('Briques', 'Tous types de briques'),
        ('Ciment', 'Ciment et liant'),
        ('Peinture', 'Peintures intérieures et extérieures'),
        ('Bois', 'Matériaux en bois'),
        ('Métal', 'Produits métalliques'),
        ('Électricité', 'Matériel électrique'),
        ('Plomberie', 'Matériel de plomberie')
    ]
    
    for categorie in categories_default:
        try:
            cursor.execute('INSERT INTO categories (nom, description) VALUES (?, ?)', categorie)
        except sqlite3.IntegrityError:
            # La catégorie existe déjà, on ignore
            pass
    
    # Valider les modifications
    conn.commit()
    conn.close()
    
    print("Base de données initialisée avec succès!")