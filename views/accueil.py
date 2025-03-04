import tkinter as tk
from tkinter import ttk
import os
import sys
from controllers.gestion_produit import GestionProduit
from controllers.gestion_stock import GestionStock
from controllers.gestion_vente import GestionVente

class AccueilView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialiser les contrôleurs
        self.gestion_produit = GestionProduit()
        self.gestion_stock = GestionStock()
        self.gestion_vente = GestionVente()
        
        # Titre
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="Gestion de Magasin - Matériaux de Construction", 
                 style="Header.TLabel").pack(side=tk.LEFT)
        
        # Menu principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Grille pour les boutons du menu
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Statistiques
        stats_frame = ttk.LabelFrame(main_frame, text="Statistiques")
        stats_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        # Créer les widgets pour les statistiques
        self.stats_produits = ttk.Label(stats_frame, text="Total Produits: 0")
        self.stats_produits.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.stats_stock = ttk.Label(stats_frame, text="Valeur du Stock: 0 DA")
        self.stats_stock.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        self.stats_ventes = ttk.Label(stats_frame, text="Ventes du jour: 0 DA")
        self.stats_ventes.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        self.stats_alerte = ttk.Label(stats_frame, text="Produits en alerte: 0")
        self.stats_alerte.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        self.stats_benefice = ttk.Label(stats_frame, text="Bénéfice mensuel: 0 DA")
        self.stats_benefice.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Mettre à jour les statistiques
        self.update_statistics()
        
        # Boutons du menu principal
        menu_frame = ttk.Frame(main_frame)
        menu_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        # Définir la taille des boutons
        button_width = 25
        button_padding = 10
        
        # Première rangée de boutons
        ttk.Button(menu_frame, text="Gestion des Produits", 
                  width=button_width, 
                  command=self.open_produits_view).grid(row=0, column=0, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Gestion des Ventes", 
                  width=button_width, 
                  command=self.open_ventes_view).grid(row=0, column=1, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Gestion des Achats", 
                  width=button_width, 
                  command=self.open_achats_view).grid(row=0, column=2, padx=button_padding, pady=button_padding)
        
        # Deuxième rangée de boutons
        ttk.Button(menu_frame, text="Gestion des Clients", 
                  width=button_width, 
                  command=self.open_clients_view).grid(row=1, column=0, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Gestion des Fournisseurs", 
                  width=button_width, 
                  command=self.open_fournisseurs_view).grid(row=1, column=1, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Rapports & Statistiques", 
                  width=button_width, 
                  command=self.open_rapports_view).grid(row=1, column=2, padx=button_padding, pady=button_padding)
        
        # Troisième rangée de boutons (facultatif)
        ttk.Button(menu_frame, text="Inventaire du Stock", 
                  width=button_width, 
                  command=self.open_inventaire_view).grid(row=2, column=0, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Paramètres", 
                  width=button_width, 
                  command=self.open_parametres_view).grid(row=2, column=1, padx=button_padding, pady=button_padding)
        
        ttk.Button(menu_frame, text="Quitter", 
                  width=button_width, 
                  command=self.quit_app).grid(row=2, column=2, padx=button_padding, pady=button_padding)
        
        # Barre de statut
        status_frame = ttk.Frame(self)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Prêt")
        self.status_label.pack(side=tk.LEFT)
        
        # Afficher la date et l'heure
        self.date_label = ttk.Label(status_frame, text="")
        self.date_label.pack(side=tk.RIGHT)
        self.update_date()
    
    def update_statistics(self):
        """Met à jour les statistiques affichées sur l'écran d'accueil"""
        try:
            # Obtenir les statistiques depuis les contrôleurs
            total_produits = self.gestion_produit.get_total_produits()
            valeur_achat, valeur_vente = self.gestion_stock.get_valeur_totale_stock()
            ventes_jour = self.gestion_vente.get_ventes_jour()
            produits_alerte = self.gestion_stock.get_produits_en_alerte()
            benefice_mensuel = self.gestion_vente.get_benefice_mensuel()
            
            # Mettre à jour les labels
            self.stats_produits.config(text=f"Total Produits: {total_produits}")
            self.stats_stock.config(text=f"Valeur du Stock: {valeur_achat:,.2f} DA (Achat), {valeur_vente:,.2f} DA (Vente)")
            self.stats_ventes.config(text=f"Ventes du jour: {ventes_jour:,.2f} DA")
            self.stats_alerte.config(text=f"Produits en alerte: {produits_alerte}")
            self.stats_benefice.config(text=f"Bénéfice mensuel: {benefice_mensuel:,.2f} DA")
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour des statistiques: {e}")
            self.status_label.config(text=f"Erreur: {e}")
    
    def update_date(self):
        """Met à jour la date et l'heure dans la barre de statut"""
        import datetime
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y %H:%M:%S")
        self.date_label.config(text=date_str)
        # Mettre à jour toutes les secondes
        self.after(1000, self.update_date)
    
    def open_produits_view(self):
        """Ouvre la vue de gestion des produits"""
        from views.produits_view import ProduitsView
        # Nettoyer la fenêtre principale
        for widget in self.parent.winfo_children():
            widget.destroy()
        # Ouvrir la nouvelle vue
        ProduitsView(self.parent)
        self.status_label.config(text="Gestion des produits ouverte")
    
    def open_ventes_view(self):
        """Ouvre la vue de gestion des ventes"""
        from views.ventes_view import VentesView
        for widget in self.parent.winfo_children():
            widget.destroy()
        VentesView(self.parent)
        self.status_label.config(text="Gestion des ventes ouverte")
    
    def open_achats_view(self):
        """Ouvre la vue de gestion des achats"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Gestion des achats (à implémenter)")
    
    def open_clients_view(self):
        """Ouvre la vue de gestion des clients"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Gestion des clients (à implémenter)")
    
    def open_fournisseurs_view(self):
        """Ouvre la vue de gestion des fournisseurs"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Gestion des fournisseurs (à implémenter)")
    
    def open_rapports_view(self):
        """Ouvre la vue des rapports et statistiques"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Rapports et statistiques (à implémenter)")
    
    def open_inventaire_view(self):
        """Ouvre la vue d'inventaire"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Inventaire du stock (à implémenter)")
    
    def open_parametres_view(self):
        """Ouvre la vue des paramètres"""
        # Implémenter quand la vue sera créée
        self.status_label.config(text="Paramètres (à implémenter)")
    
    def quit_app(self):
        """Ferme l'application"""
        if tk.messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter?"):
            self.parent.destroy()


# Pour tester cette vue individuellement
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion de Magasin - Matériaux de Construction")
    root.geometry("1024x768")
    
    # Définir un style pour l'application
    style = ttk.Style()
    style.configure("Header.TLabel", font=("Arial", 16, "bold"))
    
    app = AccueilView(root)
    root.mainloop()