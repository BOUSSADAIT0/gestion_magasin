import sqlite3

class Categorie:
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

    def save(self):
        """Insère ou met à jour une catégorie en base de données"""
        connection = sqlite3.connect("magasin.db")
        cursor = connection.cursor()
        if self.id:  # Mise à jour si ID existe
            cursor.execute("UPDATE categories SET name = ?, description = ? WHERE id = ?", 
                           (self.name, self.description, self.id))
        else:  # Insertion sinon
            cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", 
                           (self.name, self.description))
            self.id = cursor.lastrowid  # Récupérer l'ID généré
        connection.commit()
        connection.close()
        return self.id

    def delete(self):
        """Supprime la catégorie de la base de données"""
        if self.id:
            connection = sqlite3.connect("magasin.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM categories WHERE id = ?", (self.id,))
            connection.commit()
            connection.close()
            return True
        return False

    @staticmethod
    def get_all():
        """Retourne toutes les catégories"""
        connection = sqlite3.connect("magasin.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, description FROM categories")
        categories = [Categorie(*row) for row in cursor.fetchall()]
        connection.close()
        return categories

    @staticmethod
    def get_by_id(id):
        """Retourne une catégorie spécifique par son ID"""
        connection = sqlite3.connect("magasin.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, description FROM categories WHERE id = ?", (id,))
        row = cursor.fetchone()
        connection.close()
        return Categorie(*row) if row else None
