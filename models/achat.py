# models/achat.py
import sqlite3
import os
from datetime import datetime

class Achat:
    def __init__(self, id=None, fournisseur_id=None, date_achat=None, montant_total=0.0, notes=""):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.date_achat = date_achat if date_achat else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.montant_total = montant_total
        self.notes = notes
        self.details = []  # Liste des DetailAchat
    
    @staticmethod
    def get_db_connection():
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'database.db')
        return sqlite3.connect(db_path)
    
    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Nouvel achat
                cursor.execute('''
                INSERT INTO achats (fournisseur_id, date_achat, montant_total, notes) 
                VALUES (?, ?, ?, ?)
                ''', (self.fournisseur_id, self.date_achat, self.montant_total, self.notes))
                self.id = cursor.lastrowid
                
                # Ajouter les détails d'achat
                for detail in self.details:
                    detail.achat_id = self.id
                    cursor.execute('''
                    INSERT INTO details_achat (achat_id, produit_id, quantite, prix_unitaire) 
                    VALUES (?, ?, ?, ?)
                    ''', (detail.achat_id, detail.produit_id, detail.quantite, detail.prix_unitaire))
                    
                    # Mettre à jour le stock du produit
                    cursor.execute('''
                    UPDATE produits 
                    SET quantite = quantite + ? 
                    WHERE id = ?
                    ''', (detail.quantite, detail.produit_id))
                
            else:
                # Mise à jour d'un achat existant (généralement juste les notes)
                cursor.execute('''
                UPDATE achats 
                SET fournisseur_id=?, date_achat=?, montant_total=?, notes=?
                WHERE id=?
                ''', (self.fournisseur_id, self.date_achat, self.montant_total, self.notes, self.id))
            
            conn.commit()
            return self.id
            

        except sqlite3.Error as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM achats WHERE id=?', (id,))
        achat_data = cursor.fetchone()
        
        if not achat_data:
            conn.close()
            return None
        
        achat = cls(
            id=achat_data[0],
            fournisseur_id=achat_data[1],
            date_achat=achat_data[2],
            montant_total=achat_data[3],
            notes=achat_data[4]
        )
        
        # Récupérer les détails d'achat
        cursor.execute('SELECT * FROM details_achat WHERE achat_id=?', (id,))
        details_data = cursor.fetchall()
        
        conn.close()
        
        for detail_data in details_data:
            detail = DetailAchat(
                id=detail_data[0],
                achat_id=detail_data[1],
                produit_id=detail_data[2],
                quantite=detail_data[3],
                prix_unitaire=detail_data[4]
            )
            achat.details.append(detail)
        
        return achat
    
    @classmethod
    def get_all(cls, limit=100):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT a.*, f.nom 
        FROM achats a
        LEFT JOIN fournisseurs f ON a.fournisseur_id = f.id
        ORDER BY a.date_achat DESC
        LIMIT ?
        ''', (limit,))
        
        achats_data = cursor.fetchall()
        
        conn.close()
        
        return [(
            row[0],  # id
            row[1],  # fournisseur_id
            row[2],  # date_achat
            row[3],  # montant_total
            row[5]   # nom_fournisseur
        ) for row in achats_data]
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Obtenir les détails de l'achat pour ajuster le stock
            cursor.execute('SELECT produit_id, quantite FROM details_achat WHERE achat_id=?', (self.id,))
            details = cursor.fetchall()
            
            # Ajuster le stock pour chaque produit
            for produit_id, quantite in details:
                cursor.execute('''
                UPDATE produits 
                SET quantite = quantite - ? 
                WHERE id = ?
                ''', (quantite, produit_id))
            
            # Supprimer les détails d'achat
            cursor.execute('DELETE FROM details_achat WHERE achat_id=?', (self.id,))
            
            # Supprimer l'achat
            cursor.execute('DELETE FROM achats WHERE id=?', (self.id,))
            
            conn.commit()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()

class DetailAchat:
    def __init__(self, id=None, achat_id=None, produit_id=None, quantite=0, prix_unitaire=0.0):
        self.id = id
        self.achat_id = achat_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire

# models/categorie.py
import sqlite3
import os

class Categorie:
    def __init__(self, id=None, nom="", description=""):
        self.id = id
        self.nom = nom
        self.description = description
    
    @staticmethod
    def get_db_connection():
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'database.db')
        return sqlite3.connect(db_path)
    
    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            # Nouvelle catégorie
            cursor.execute('''
            INSERT INTO categories (nom, description) 
            VALUES (?, ?)
            ''', (self.nom, self.description))
            self.id = cursor.lastrowid
        else:
            # Mise à jour d'une catégorie existante
            cursor.execute('''
            UPDATE categories 
            SET nom=?, description=?
            WHERE id=?
            ''', (self.nom, self.description, self.id))
        
        conn.commit()
        conn.close()
        return self.id
    
    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories ORDER BY nom')
        categories_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            description=row[2]
        ) for row in categories_data]
    
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories WHERE id=?', (id,))
        categorie_data = cursor.fetchone()
        
        conn.close()
        
        if categorie_data:
            return cls(
                id=categorie_data[0],
                nom=categorie_data[1],
                description=categorie_data[2]
            )
        return None
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Vérifier si des produits utilisent cette catégorie
            cursor.execute('SELECT COUNT(*) FROM produits WHERE categorie_id=?', (self.id,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Il existe des produits utilisant cette catégorie
                conn.close()
                return False
            
            cursor.execute('DELETE FROM categories WHERE id=?', (self.id,))
            conn.commit()
            result = cursor.rowcount > 0
            
        except sqlite3.Error:
            result = False
        finally:
            conn.close()
        
        return result