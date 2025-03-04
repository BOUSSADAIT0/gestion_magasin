# models/produit.py
import sqlite3
import os

class Produit:
    def __init__(self, id=None, nom="", description="", categorie_id=None, 
                 prix_achat=0.0, prix_vente=0.0, quantite=0, seuil_reapprovisionnement=5):
        self.id = id
        self.nom = nom
        self.description = description
        self.categorie_id = categorie_id
        self.prix_achat = prix_achat
        self.prix_vente = prix_vente
        self.quantite = quantite
        self.seuil_reapprovisionnement = seuil_reapprovisionnement
    
    @staticmethod
    def get_db_connection():
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'database.db')
        return sqlite3.connect(db_path)
    
    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # Nouveau produit
            cursor.execute('''
            INSERT INTO produits 
            (nom, description, categorie_id, prix_achat, prix_vente, quantite, seuil_reapprovisionnement) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.nom, self.description, self.categorie_id, self.prix_achat, 
                 self.prix_vente, self.quantite, self.seuil_reapprovisionnement))
            self.id = cursor.lastrowid
        else:
            # Mise à jour d'un produit existant
            cursor.execute('''
            UPDATE produits 
            SET nom=?, description=?, categorie_id=?, prix_achat=?, prix_vente=?, 
                quantite=?, seuil_reapprovisionnement=?
            WHERE id=?
            ''', (self.nom, self.description, self.categorie_id, self.prix_achat, 
                 self.prix_vente, self.quantite, self.seuil_reapprovisionnement, self.id))
        
        conn.commit()
        conn.close()
        return self.id
    
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM produits WHERE id=?', (id,))
        produit_data = cursor.fetchone()
        
        conn.close()
        
        if produit_data:
            return cls(
                id=produit_data[0],
                nom=produit_data[1],
                description=produit_data[2],
                categorie_id=produit_data[3],
                prix_achat=produit_data[4],
                prix_vente=produit_data[5],
                quantite=produit_data[6],
                seuil_reapprovisionnement=produit_data[7]
            )
        return None
    
    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM produits')
        produits_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            description=row[2],
            categorie_id=row[3],
            prix_achat=row[4],
            prix_vente=row[5],
            quantite=row[6],
            seuil_reapprovisionnement=row[7]
        ) for row in produits_data]
    
    @classmethod
    def get_by_category(cls, categorie_id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM produits WHERE categorie_id=?', (categorie_id,))
        produits_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            description=row[2],
            categorie_id=row[3],
            prix_achat=row[4],
            prix_vente=row[5],
            quantite=row[6],
            seuil_reapprovisionnement=row[7]
        ) for row in produits_data]
    
    @classmethod
    def search(cls, term):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM produits 
        WHERE nom LIKE ? OR description LIKE ?
        ''', (f'%{term}%', f'%{term}%'))
        
        produits_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            description=row[2],
            categorie_id=row[3],
            prix_achat=row[4],
            prix_vente=row[5],
            quantite=row[6],
            seuil_reapprovisionnement=row[7]
        ) for row in produits_data]
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM produits WHERE id=?', (self.id,))
            conn.commit()
            result = cursor.rowcount > 0
        except sqlite3.Error:
            result = False
        finally:
            conn.close()
        
        return result
    
    @classmethod
    def get_produits_faible_stock(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM produits 
        WHERE quantite <= seuil_reapprovisionnement
        ''')
        
        produits_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            description=row[2],
            categorie_id=row[3],
            prix_achat=row[4],
            prix_vente=row[5],
            quantite=row[6],
            seuil_reapprovisionnement=row[7]
        ) for row in produits_data]
    
    @classmethod
    def mettre_a_jour_stock(cls, produit_id, quantite_ajout):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE produits 
        SET quantite = quantite + ? 
        WHERE id = ?
        ''', (quantite_ajout, produit_id))
        
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
