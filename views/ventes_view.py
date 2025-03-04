import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from datetime import datetime, timedelta

# Ajouter le chemin parent au sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from controllers.gestion_vente import GestionVente
from controllers.gestion_produit import GestionProduit
from controllers.gestion_stock import GestionStock

class VentesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialiser les contrôleurs
        self.gestion_vente = GestionVente()
        self.gestion_produit = GestionProduit()
        self.gestion_stock = GestionStock()
        
        # Définir les variables
        self.search_var = tk.StringVar()
        self.date_debut_var = tk.StringVar()
        self.date_fin_var = tk.StringVar()
        self.client_var = tk.StringVar()
        
        # Variables pour la nouvelle vente
        self.panier = []
        self.total_vente = 0.0
        
        # Créer l'interface
        self.create_widgets()
        
        # Par défaut, afficher les ventes du jour
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_debut_var.set(today)
        self.date_fin_var.set(today)
        self.load_ventes()
    
    def create_widgets(self):
        # Créer un notebook (onglets)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet 1: Liste des Ventes
        self.tab_liste = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_liste, text="Liste des Ventes")
        
        # Onglet 2: Nouvelle Vente
        self.tab_nouvelle = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_nouvelle, text="Nouvelle Vente")
        
        # Configurer l'onglet Liste des Ventes
        self.setup_liste_ventes_tab()
        
        # Configurer l'onglet Nouvelle Vente
        self.setup_nouvelle_vente_tab()
        
        # Bouton retour (en dehors des onglets)
        self.bouton_retour = ttk.Button(self, text="Retour à l'Accueil", command=self.return_to_home)
        self.bouton_retour.pack(side=tk.BOTTOM, anchor=tk.W, padx=20, pady=10)
    
    def setup_liste_ventes_tab(self):
        # Titre
        header_frame = ttk.Frame(self.tab_liste)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Historique des Ventes", style="Header.TLabel").pack(side=tk.LEFT)
        
        # Filtres et recherche
        filter_frame = ttk.LabelFrame(self.tab_liste, text="Filtres")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Période
        periode_frame = ttk.Frame(filter_frame)
        periode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(periode_frame, text="Du:").grid(row=0, column=0, padx=5, pady=5)
        date_debut = ttk.Entry(periode_frame, textvariable=self.date_debut_var, width=12)
        date_debut.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(periode_frame, text="Au:").grid(row=0, column=2, padx=5, pady=5)
        date_fin = ttk.Entry(periode_frame, textvariable=self.date_fin_var, width=12)
        date_fin.grid(row=0, column=3, padx=5, pady=5)
        
        # Bouton de recherche
        btn_rechercher = ttk.Button(periode_frame, text="Rechercher", command=self.load_ventes)
        btn_rechercher.grid(row=0, column=4, padx=5, pady=5)
        
        # Tableau des ventes
        self.tableau_ventes = ttk.Treeview(self.tab_liste, columns=("date", "client", "total"), show="headings")
        self.tableau_ventes.heading("date", text="Date")
        self.tableau_ventes.heading("client", text="Client")
        self.tableau_ventes.heading("total", text="Total")
        self.tableau_ventes.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Barre de défilement pour le tableau
        scrollbar = ttk.Scrollbar(self.tab_liste, orient="vertical", command=self.tableau_ventes.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tableau_ventes.configure(yscrollcommand=scrollbar.set)
    
    def load_ventes(self):
        # Effacer le tableau
        for row in self.tableau_ventes.get_children():
            self.tableau_ventes.delete(row)
        
        # Récupérer les dates de début et de fin
        date_debut = self.date_debut_var.get()
        date_fin = self.date_fin_var.get()
        
        # Vérification de la validité des dates
        try:
            date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d")
            date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erreur de date", "Veuillez entrer des dates au format AAAA-MM-JJ.")
            return
        
        if date_debut_obj > date_fin_obj:
            messagebox.showerror("Erreur de date", "La date de début doit être avant la date de fin.")
            return
        
        # Charger les ventes depuis le contrôleur
        ventes = self.gestion_vente.get_ventes(date_debut, date_fin)
        
        # Afficher les ventes dans le tableau
        for vente in ventes:
            self.tableau_ventes.insert("", tk.END, values=(vente['date'], vente['client'], vente['total']))
    
    def setup_nouvelle_vente_tab(self):
        # Titre
        ttk.Label(self.tab_nouvelle, text="Nouvelle Vente", style="Header.TLabel").pack(pady=10)
        
        # Sélection du produit
        product_frame = ttk.LabelFrame(self.tab_nouvelle, text="Produits disponibles")
        product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tableau_produits = ttk.Treeview(product_frame, columns=("nom", "prix", "stock"), show="headings")
        self.tableau_produits.heading("nom", text="Nom")
        self.tableau_produits.heading("prix", text="Prix")
        self.tableau_produits.heading("stock", text="Stock")
        self.tableau_produits.pack(fill=tk.BOTH, expand=True)
        
        # Chargement des produits
        self.load_produits()
    
    def load_produits(self):
        produits = self.gestion_produit.get_all()
        for produit in produits:
            self.tableau_produits.insert("", tk.END, values=(produit['nom'], produit['prix'], produit['stock']))
    
    def return_to_home(self):
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion des Ventes")
    root.geometry("800x600")
    app = VentesView(root)
    root.mainloop()
