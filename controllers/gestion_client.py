
# controllers/gestion_client.py
from models.client import Client

class GestionClient:
    @staticmethod
    def ajouter_client(nom, adresse="", telephone="", email="", notes=""):
        """
        Ajoute un nouveau client
        
        Returns:
            (success, client_id, message)
        """
        try:
            client = Client(
                nom=nom,
                adresse=adresse,
                telephone=telephone,
                email=email,
                notes=notes
            )
            client_id = client.save()
            return True, client_id, "Client ajouté avec succès."
        except Exception as e:
            return False, None, f"Erreur lors de l'ajout du client: {str(e)}"
    
    @staticmethod
    def modifier_client(id, nom, adresse="", telephone="", email="", notes=""):
        """
        Modifie un client existant
        
        Returns:
            (success, message)
        """
        try:
            client = Client.get_by_id(id)
            if not client:
                return False, "Client non trouvé."
            
            client.nom = nom
            client.adresse = adresse
            client.telephone = telephone
            client.email = email
            client.notes = notes
            
            client.save()
            return True, "Client modifié avec succès."
        except Exception as e:
            return False, f"Erreur lors de la modification du client: {str(e)}"
    
    @staticmethod
    def supprimer_client(id):
        """
        Supprime un client
        
        Returns:
            (success, message)
        """
        try:
            client = Client.get_by_id(id)
            if not client:
                return False, "Client non trouvé."
            
            if client.delete():
                return True, "Client supprimé avec succès."
            else:
                return False, "Impossible de supprimer le client (peut avoir des ventes associées)."
        except Exception as e:
            return False, f"Erreur lors de la suppression du client: {str(e)}"
    
    @staticmethod
    def rechercher_clients(terme):
        """
        Recherche des clients par terme
        
        Returns:
            Liste de clients
        """
        return Client.search(terme)
    
    @staticmethod
    def obtenir_tous_clients():
        """
        Récupère tous les clients
        
        Returns:
            Liste de clients
        """
        return Client.get_all()
    
    @staticmethod
    def obtenir_client_par_id(id):
        """
        Récupère un client par son ID
        
        Returns:
            Objet Client ou None
        """
        return Client.get_by_id(id)
    
    @staticmethod
    def obtenir_historique_achats(client_id):
        """
        Récupère l'historique des achats d'un client
        
        Returns:
            Liste de ventes
        """
        client = Client.get_by_id(client_id)
        if not client:
            return []
        
        return client.get_historique_achats()
