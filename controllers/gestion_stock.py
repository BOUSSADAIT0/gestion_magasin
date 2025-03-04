# controllers/gestion_stock.py
from models.produit import Produit
import sqlite3
from datetime import datetime

class GestionStock:
    @staticmethod
    def obtenir_etat_stock():
        """
        Récupère l'état actuel du stock
        
        Returns:
            Liste de produits avec leur niveau de stock
        """
        return Produit.get_all()
    
    @staticmethod
    def obtenir_produits_faible_stock():
        """
        Récupère les produits dont le stock est inférieur ou égal au seuil de réapprovisionnement
        
        Returns:
            Liste de produits avec stock faible
        """
        return Produit.get_produits_faible_stock()
    
    @staticmethod
    def ajuster_stock(produit_id, quantite_ajout, raison="Ajustement manuel"):
        """
        Ajuste le stock d'un produit
        
        Args:
            produit_id: ID du produit
            quantite_ajout: Quantité à ajouter (peut être négative pour une réduction)
            raison: Raison de l'ajustement
            
        Returns:
            (success, message)
        """
        try:
            produit = Produit.get_by_id(produit_id)
            if not produit:
                return False, "Produit non trouvé."
            
            # Vérifier que l'ajustement ne donne pas un stock négatif
            if produit.quantite + quantite_ajout < 0:
                return False, "L'ajustement donnerait un stock négatif."
            
            if Produit.mettre_a_jour_stock(produit_id, quantite_ajout):
                return True, "Stock ajusté avec succès."
            else:
                return False, "Erreur lors de l'ajustement du stock."
                
        except Exception as e:
            return False, f"Erreur lors de l'ajustement du stock: {str(e)}"
    
    @staticmethod
    def verifier_disponibilite(produit_id, quantite_demandee):
        """
        Vérifie si un produit est disponible en quantité suffisante
        
        Args:
            produit_id: ID du produit
            quantite_demandee: Quantité demandée
            
        Returns:
            (disponible, message)
        """
        produit = Produit.get_by_id(produit_id)
        if not produit:
            return False, "Produit non trouvé."
        
        if produit.quantite >= quantite_demandee:
            return True, f"Produit disponible ({produit.quantite} en stock)"
        else:
            return False, f"Stock insuffisant (Disponible: {produit.quantite}, Demandé: {quantite_demandee})"
    
    @staticmethod
    def get_valeur_totale_stock():
        """
        Calcule la valeur totale du stock
        
        Returns:
            (valeur_achat, valeur_vente)
        """
        produits = Produit.get_all()
        
        valeur_achat = sum(p.prix_achat * p.quantite for p in produits)
        valeur_vente = sum(p.prix_vente * p.quantite for p in produits)
        
        return valeur_achat, valeur_vente

    @staticmethod
    def get_produits_en_alerte():
        """
        Récupère les produits en alerte de stock
        
        Returns:
            Liste de produits en alerte
        """
        return Produit.get_produits_faible_stock()