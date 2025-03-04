# controllers/gestion_achat.py
import sqlite3
from datetime import datetime
from models.achat import Achat, DetailAchat
from models.fournisseur import Fournisseur
from models.produit import Produit

class GestionAchat:
    @staticmethod
    def creer_achat(fournisseur_id, produits_quantites_prix, notes=""):
        """
        Crée un nouvel achat
        
        Args:
            fournisseur_id: ID du fournisseur
            produits_quantites_prix: Liste de tuples (produit_id, quantite, prix_unitaire)
            notes: Notes sur l'achat
            
        Returns:
            (success, achat_id, message)
        """
        try:
            # Vérifier si le fournisseur existe
            fournisseur = Fournisseur.get_by_id(fournisseur_id)
            if not fournisseur:
                return False, None, "Fournisseur non trouvé."
            
            # Créer l'achat
            achat = Achat(fournisseur_id=fournisseur_id, notes=notes)
            
            # Ajouter les détails d'achat
            montant_total = 0
            for produit_id, quantite, prix_unitaire in produits_quantites_prix:
                produit = Produit.get_by_id(produit_id)
                if not produit:
                    return False, None, f"Produit ID {produit_id} non trouvé."
                
                # Créer le détail d'achat
                detail = DetailAchat(
                    produit_id=produit_id,
                    quantite=quantite,
                    prix_unitaire=prix_unitaire
                )
                
                achat.details.append(detail)
                montant_total += quantite * prix_unitaire
            
            achat.montant_total = montant_total
            achat_id = achat.save()
            
            return True, achat_id, "Achat enregistré avec succès."
            
        except Exception as e:
            return False, None, f"Erreur lors de la création de l'achat: {str(e)}"
    
    @staticmethod
    def annuler_achat(achat_id):
        """
        Annule un achat et ajuste le stock des produits
        
        Args:
            achat_id: ID de l'achat à annuler
            
        Returns:
            (success, message)
        """
        try:
            achat = Achat.get_by_id(achat_id)
            if not achat:
                return False, "Achat non trouvé."
            
            if achat.delete():
                return True, "Achat annulé avec succès."
            else:
                return False, "Erreur lors de l'annulation de l'achat."
                
        except Exception as e:
            return False, f"Erreur lors de l'annulation de l'achat: {str(e)}"
    
    @staticmethod
    def obtenir_achats_recents(limit=100):
        """
        Récupère les achats récents
        
        Args:
            limit: Nombre maximum d'achats à récupérer
            
        Returns:
            Liste d'achats
        """
        return Achat.get_all(limit)
    
    @staticmethod
    def obtenir_achat_details(achat_id):
        """
        Récupère les détails d'un achat
        
        Args:
            achat_id: ID de l'achat
            
        Returns:
            Objet Achat avec ses détails
        """
        return Achat.get_by_id(achat_id)
