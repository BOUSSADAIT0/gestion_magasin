
# models/client.py
import sqlite3
import os
from datetime import datetime

class Client:
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
            INSERT INTO clients (nom, adresse, telephone, email, notes) 
            VALUES (?, ?, ?, ?, ?)
            ''', (self.nom, self.adresse, self.telephone, self.email, self.notes))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
            UPDATE clients 
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
        
        cursor.execute('SELECT * FROM clients')
        clients_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            adresse=row[2],
            telephone=row[3],
            email=row[4],
            notes=row[5]
        ) for row in clients_data]
    
    @classmethod
    def get_by_id(cls, id):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clients WHERE id=?', (id,))
        client_data = cursor.fetchone()
        
        conn.close()
        
        if client_data:
            return cls(
                id=client_data[0],
                nom=client_data[1],
                adresse=client_data[2],
                telephone=client_data[3],
                email=client_data[4],
                notes=client_data[5]
            )
        return None
    
    @classmethod
    def search(cls, term):
        conn = cls.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM clients 
        WHERE nom LIKE ? OR adresse LIKE ? OR telephone LIKE ? OR email LIKE ?
        ''', (f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
        
        clients_data = cursor.fetchall()
        
        conn.close()
        
        return [cls(
            id=row[0],
            nom=row[1],
            adresse=row[2],
            telephone=row[3],
            email=row[4],
            notes=row[5]
        ) for row in clients_data]
    
    def delete(self):
        if self.id is None:
            return False
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM clients WHERE id=?', (self.id,))
            conn.commit()
            result = cursor.rowcount > 0
        except sqlite3.Error:
            result = False
        finally:
            conn.close()
        
        return result
    
    def get_historique_achats(self):
        from models.vente import Vente
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM ventes 
        WHERE client_id=?
        ORDER BY date_vente DESC
        ''', (self.id,))
        
        ventes_data = cursor.fetchall()
        
        conn.close()
        
        return [Vente(
            id=row[0],
            client_id=row[1],
            date_vente=row[2],
            montant_total=row[3],
            notes=row[4]
        ) for row in ventes_data]
