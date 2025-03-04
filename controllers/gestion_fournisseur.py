
# controllers/gestion_fournisseur.py
from models.fournisseur import Fournisseur

class GestionFournisseur:
    @staticmethod
    def ajouter_fournisseur(nom, adresse="", telephone="", email="", notes=""):
        """
        Ajoute un nouveau fournisseur
        
        Returns:
            (success, fournisseur_id, message)
        """
        try:
            fournisseur = Fournisseur(
                nom=nom,
                adresse=adresse,
                telephone=telephone,
                email=email,
                notes=notes
            )
            fournisseur_id = fournisseur.save()
            return True, fournisseur_id, "Fournisseur ajouté avec succès."
        except Exception as e:
            return False, None, f"Erreur lors de l'ajout du fournisseur: {str(e)}"
    
    @staticmethod
    def modifier_fournisseur(id, nom, adresse="", telephone="", email="", notes=""):
        """
        Modifie un fournisseur existant
        
        Returns:
            (success, message)
        """
        try:
            fournisseur = Fournisseur.get_by_id(id)
            if not fournisseur:
                return False, "Fournisseur non trouvé."
            
            fournisseur.nom = nom
            fournisseur.adresse = adresse
            fournisseur.telephone = telephone
            fournisseur.email = email
            fournisseur.notes = notes
            
            fournisseur.save()
            return True, "Fournisseur modifié avec succès."
        except Exception as e:
            return False, f"Erreur lors de la modification du fournisseur: {str(e)}"
    
    @staticmethod
    def supprimer_fournisseur(id):
        """
        Supprime un fournisseur
        
        Returns:
            (success, message)
        """
        try:
            fournisseur = Fournisseur.get_by_id(id)
            if not fournisseur:
                return False, "Fournisseur non trouvé."
            
            if fournisseur.delete():
                return True, "Fournisseur supprimé avec succès."
            else:
                return False, "Impossible de supprimer le fournisseur (peut avoir des achats associés)."
        except Exception as e:
            return False, f"Erreur lors de la suppression du fournisseur: {str(e)}"
    
    @staticmethod
    def obtenir_tous_fournisseurs():
        """
        Récupère tous les fournisseurs
        
        Returns:
            Liste de fournisseurs
        """
        return Fournisseur.get_all()
    
    @staticmethod
    def obtenir_fournisseur_par_id(id):
        """
        Récupère un fournisseur par son ID
        
        Returns:
            Objet Fournisseur ou None
        """
        return Fournisseur.get_by_id(id)

