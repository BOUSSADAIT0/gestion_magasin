import sqlite3
import os
from datetime import datetime

class Vente:
    def __init__(self, id=None, client_id=None, date_vente=None, montant_total=0.0, notes=""):
        self.id = id
        self.client_id = client_id
        self.date_vente = date_vente if date_vente else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.montant_total = montant_total
        self.notes = notes
        self.details = []  # Liste des DetailVente
    
    @staticmethod
    def get_db_connection():
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'database.db')
        return sqlite3.connect(db_path)
    
    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id is None:
                # Nouvelle vente
                cursor.execute('''
                INSERT INTO ventes (client_id, date_vente, montant_total, notes) 
                VALUES (?, ?, ?, ?)
                ''', (self.client_id, self.date_vente, self.montant_total, self.notes))
                self.id = cursor.lastrowid
                
                # Ajouter les détails de vente
                for detail in self.details:
                    detail.vente_id = self.id
                    cursor.execute('''
                    INSERT INTO details_vente (vente_id, produit_id, quantite, prix_unitaire) 
                    VALUES (?, ?, ?, ?)
                    ''', (detail.vente_id, detail.produit_id, detail.quantite, detail.prix_unitaire))
                    
                    # Mettre à jour le stock du produit
                    cursor.execute('''
                    UPDATE produits 
                    SET quantite = quantite - ? 
                    WHERE id = ?
                    ''', (detail.quantite, detail.produit_id))
                
            else:
                # Mise à jour d'une vente existante (généralement juste les notes)
                cursor.execute('''
                UPDATE ventes 
                SET client_id=?, date_vente=?, montant_total=?, notes=?
                WHERE id=?
                ''', (self.client_id, self.date_vente, self.montant_total, self.notes, self.id))
            
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
        
        cursor.execute('SELECT * FROM ventes WHERE id=?', (id,))
        vente_data = cursor.fetchone()
        
        if not vente_data:
            conn.close()
            return None
        
        vente = cls(
            id=vente_data[0],
            client_id=vente_data[1],
            date_vente=vente_data[2],
            montant_total=vente_data[3],
            notes=vente_data[4]
        )
        
        # Récupérer les détails de vente
        cursor.execute('SELECT * FROM details_vente WHERE vente_id=?', (id,))
        details_data = cursor.fetchall()
        
        conn.close()
        
        for detail_data in details_data:
            detail = DetailVente(
                id=detail_data[0],
                vente_id=detail_data[1],
                produit_id=detail_data[2],
                quantite=detail_data[3],
                prix_unitaire=detail_data[4]
            )
            vente.details.append(detail)
        
        return vente
    
    @classmethod
    def get_all(cls, limit=100):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT v.*, c.nom 
        FROM ventes v
        LEFT JOIN clients c ON v.client_id = c.id
        ORDER BY v.date_vente DESC
        LIMIT ?
        ''', (limit,))
        
        ventes_data = cursor.fetchall()
        
        conn.close()
        
        return [(
            row[0],  # id
            row[1],  # client_id
            row[2],  # date_vente
            row[3],  # montant_total
            row[5]   # nom_client
        ) for row in ventes_data]
    
    @classmethod
    def get_ventes_periode(cls, date_debut, date_fin):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT v.*, c.nom 
        FROM ventes v
        LEFT JOIN clients c ON v.client_id = c.id
        WHERE v.date_vente BETWEEN ? AND ?
        ORDER BY v.date_vente DESC
        ''', (date_debut, date_fin))
        
        ventes_data = cursor.fetchall()
        
        conn.close()
        
        return [(
            row[0],  # id
            row[1],  # client_id
            row[2],  # date_vente
            row[3],  # montant_total
            row[5]   # nom_client
        ) for row in ventes_data]
    
    @classmethod
    def get_ventes_jour(cls):
        today = datetime.now().strftime('%Y-%m-%d')
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM ventes WHERE date_vente LIKE ?
        ''', (f'{today}%',))
        
        ventes_data = cursor.fetchall()
        conn.close()
        
        return [cls(
            id=row[0],
            client_id=row[1],
            date_vente=row[2],
            montant_total=row[3],
            notes=row[4]
        ) for row in ventes_data]
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Obtenir les détails de la vente pour rétablir le stock
            cursor.execute('SELECT produit_id, quantite FROM details_vente WHERE vente_id=?', (self.id,))
            details = cursor.fetchall()
            
            # Rétablir le stock pour chaque produit
            for produit_id, quantite in details:
                cursor.execute('''
                UPDATE produits 
                SET quantite = quantite + ? 
                WHERE id = ?
                ''', (quantite, produit_id))
            
            # Supprimer les détails de vente
            cursor.execute('DELETE FROM details_vente WHERE vente_id=?', (self.id,))
            
            # Supprimer la vente
            cursor.execute('DELETE FROM ventes WHERE id=?', (self.id,))
            
            conn.commit()
            return True
            
        except sqlite3.Error:
            conn.rollback()
            return False
        finally:
            conn.close()

class DetailVente:
    def __init__(self, id=None, vente_id=None, produit_id=None, quantite=0, prix_unitaire=0.0):
        self.id = id
        self.vente_id = vente_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire