# controllers/gestion_produit.py
import sqlite3
from models.produit import Produit
from models.categorie import Categorie

class GestionProduit:
    @staticmethod
    def ajouter_produit(nom, description, categorie_id, prix_achat, prix_vente, quantite, seuil_reapprovisionnement):
        try:
            produit = Produit(
                nom=nom,
                description=description,
                categorie_id=categorie_id,
                prix_achat=float(prix_achat),
                prix_vente=float(prix_vente),
                quantite=int(quantite),
                seuil_reapprovisionnement=int(seuil_reapprovisionnement)
            )
            produit_id = produit.save()
            return True, produit_id, "Produit ajouté avec succès."
        except (ValueError, sqlite3.Error) as e:
            return False, None, f"Erreur lors de l'ajout du produit: {str(e)}"
    
    @staticmethod
    def modifier_produit(id, nom, description, categorie_id, prix_achat, prix_vente, quantite, seuil_reapprovisionnement):
        try:
            produit = Produit.get_by_id(id)
            if not produit:
                return False, None, "Produit non trouvé."
            
            produit.nom = nom
            produit.description = description
            produit.categorie_id = categorie_id
            produit.prix_achat = float(prix_achat)
            produit.prix_vente = float(prix_vente)
            produit.quantite = int(quantite)
            produit.seuil_reapprovisionnement = int(seuil_reapprovisionnement)
            
            produit.save()
            return True, id, "Produit modifié avec succès."
        except (ValueError, sqlite3.Error) as e:
            return False, None, f"Erreur lors de la modification du produit: {str(e)}"
    
    @staticmethod
    def supprimer_produit(id):
        try:
            produit = Produit.get_by_id(id)
            if not produit:
                return False, "Produit non trouvé."
            
            if produit.delete():
                return True, "Produit supprimé avec succès."
            else:
                return False, "Impossible de supprimer le produit."
        except sqlite3.Error as e:
            return False, f"Erreur lors de la suppression du produit: {str(e)}"
    
    @staticmethod
    def rechercher_produits(terme):
        return Produit.search(terme)
    
    @staticmethod
    def obtenir_tous_produits():
        return Produit.get_all()
    
    @staticmethod
    def obtenir_produit_par_id(id):
        return Produit.get_by_id(id)
    
    @staticmethod
    def obtenir_produits_par_categorie(categorie_id):
        return Produit.get_by_category(categorie_id)
    
    @staticmethod
    def obtenir_produits_faible_stock():
        return Produit.get_produits_faible_stock()
    
    @staticmethod
    def mettre_a_jour_stock(produit_id, quantite_ajout):
        try:
            success = Produit.mettre_a_jour_stock(produit_id, quantite_ajout)
            if success:
                return True, "Stock mis à jour avec succès."
            else:
                return False, "Erreur lors de la mise à jour du stock."
        except sqlite3.Error as e:
            return False, f"Erreur de base de données: {str(e)}"
    
    @staticmethod
    def obtenir_toutes_categories():
        return Categorie.get_all()
    
    @staticmethod
    def ajouter_categorie(nom, description):
        try:
            categorie = Categorie(nom=nom, description=description)
            categorie_id = categorie.save()
            return True, categorie_id, "Catégorie ajoutée avec succès."
        except sqlite3.Error as e:
            return False, None, f"Erreur lors de l'ajout de la catégorie: {str(e)}"

    @staticmethod
    def get_total_produits():
        try:
            return len(Produit.get_all())
        except sqlite3.Error as e:
            return f"Erreur: {str(e)}"
