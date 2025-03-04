
# models/fournisseur.py
import sqlite3
import os
from datetime import datetime

class Fournisseur:
    def __init__(self, id=None, nom="", adresse="", telephone="", email="", notes=""):
        self.id = id
        self.nom = nom
        self.adresse = adresse
        self.telephone = telephone
        self.email = email
        self.notes = notes
    
    @staticmethod
    def get_db_connection():
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'database.db')
        return sqlite3.connect(db_path)
    
    def save(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute('''
            INSERT INTO fournisseurs (nom, adresse, telephone, email, notes) 
            VALUES (?, ?, ?, ?, ?)
            ''', (self.nom, self.adresse, self.telephone, self.email, self.notes))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
            UPDATE fournisseurs 
            SET nom=?, adresse=?, telephone=?, email=?, notes=?
            WHERE id=?
            ''', (self.nom, self.adresse, self.telephone, self.email, self.notes, self.id))
        
        conn.commit()
        conn.close()
        return self.id
    
    @classmethod
    def get_all(cls):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM fournisseurs')
        fournisseurs_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            adresse=row[2],
            telephone=row[3],
            email=row[4],
            notes=row[5]
        ) for row in fournisseurs_data]
    
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM fournisseurs WHERE id=?', (id,))
        fournisseur_data = cursor.fetchone()
        
        conn.close()
        
        if fournisseur_data:
            return cls(
                id=fournisseur_data[0],
                nom=fournisseur_data[1],
                adresse=fournisseur_data[2],
                telephone=fournisseur_data[3],
                email=fournisseur_data[4],
                notes=fournisseur_data[5]
            )
        return None
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM fournisseurs WHERE id=?', (self.id,))
            conn.commit()
            result = cursor.rowcount > 0
        except sqlite3.Error:
            result = False
        finally:
            conn.close()
        
        return result
