
# controllers/gestion_vente.py
import sqlite3
from models.vente import Vente, DetailVente
from models.client import Client
from models.produit import Produit
from datetime import date

class GestionVente:
    
    @staticmethod
    def creer_vente(client_id, produits_quantites, notes=""):
        """
        Crée une nouvelle vente
        
        Args:
            client_id: ID du client
            produits_quantites: Liste de tuples (produit_id, quantite)
            notes: Notes sur la vente
            
        Returns:
            (success, vente_id, message)
        """
        try:
            # Vérifier si le client existe
            client = Client.get_by_id(client_id)
            if not client:
                return False, None, "Client non trouvé."
            
            # Créer la vente
            vente = Vente(client_id=client_id, notes=notes)
            
            # Ajouter les détails de vente
            montant_total = 0
            for produit_id, quantite in produits_quantites:
                produit = Produit.get_by_id(produit_id)
                if not produit:
                    return False, None, f"Produit ID {produit_id} non trouvé."
                
                # Vérifier si le stock est suffisant
                if produit.quantite < quantite:
                    return False, None, f"Stock insuffisant pour {produit.nom} (Disponible: {produit.quantite}, Demandé: {quantite})."
                
                # Créer le détail de vente
                detail = DetailVente(
                    produit_id=produit_id,
                    quantite=quantite,
                    prix_unitaire=produit.prix_vente
                )
                
                vente.details.append(detail)
                montant_total += quantite * produit.prix_vente
            
            vente.montant_total = montant_total
            vente_id = vente.save()
            
            return True, vente_id, "Vente enregistrée avec succès."
            
        except Exception as e:
            return False, None, f"Erreur lors de la création de la vente: {str(e)}"
    
    @staticmethod
    def annuler_vente(vente_id):
        """
        Annule une vente et rétablit le stock des produits
        
        Args:
            vente_id: ID de la vente à annuler
            
        Returns:
            (success, message)
        """
        try:
            vente = Vente.get_by_id(vente_id)
            if not vente:
                return False, "Vente non trouvée."
            
            if vente.delete():
                return True, "Vente annulée avec succès."
            else:
                return False, "Erreur lors de l'annulation de la vente."
                
        except Exception as e:
            return False, f"Erreur lors de l'annulation de la vente: {str(e)}"
    
    @staticmethod
    def obtenir_ventes_recentes(limit=100):
        """
        Récupère les ventes récentes
        
        Args:
            limit: Nombre maximum de ventes à récupérer
            
        Returns:
            Liste de ventes
        """
        return Vente.get_all(limit)
    
    @staticmethod
    def obtenir_ventes_periode(date_debut, date_fin):
        """
        Récupère les ventes sur une période donnée
        
        Args:
            date_debut: Date de début (format YYYY-MM-DD)
            date_fin: Date de fin (format YYYY-MM-DD)
            
        Returns:
            Liste de ventes
        """
        return Vente.get_ventes_periode(date_debut, date_fin)
    
    @staticmethod
    def obtenir_vente_details(vente_id):
        """
        Récupère les détails d'une vente
        
        Args:
            vente_id: ID de la vente
            
        Returns:
            Objet Vente avec ses détails
        """
        return Vente.get_by_id(vente_id)

    @staticmethod
    def get_ventes_jour():
        try:
            today = date.today().strftime("%Y-%m-%d")
            ventes = Vente.get_ventes_jour()
            total = sum(v.prix_total for v in ventes)
            return total
        except sqlite3.Error as e:
            return f"Erreur: {str(e)}"
        
    @staticmethod
    def get_benefice_mensuel():
        """
        Calcule le bénéfice mensuel
        
        Returns:
            Bénéfice mensuel
        """
        try:
            conn = Vente.get_db_connection()
            cursor = conn.cursor()
            
            # Calculer le bénéfice pour le mois en cours
            cursor.execute('''
            SELECT SUM((dv.prix_unitaire - p.prix_achat) * dv.quantite) AS benefice
            FROM details_vente dv
            JOIN produits p ON dv.produit_id = p.id
            JOIN ventes v ON dv.vente_id = v.id
            WHERE strftime('%Y-%m', v.date_vente) = strftime('%Y-%m', 'now')
            ''')
            
            benefice = cursor.fetchone()[0] or 0.0
            conn.close()
            return benefice
        except sqlite3.Error as e:
            return f"Erreur: {str(e)}"