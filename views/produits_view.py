import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
from datetime import datetime

# Ajouter le chemin parent au sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from controllers.gestion_produit import GestionProduit
from controllers.gestion_stock import GestionStock

class ProduitsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialiser les contrôleurs
        self.gestion_produit = GestionProduit()
        self.gestion_stock = GestionStock()
        
        # Variables
        self.search_var = tk.StringVar()
        self.category_var = tk.StringVar()
        
        # Configurer les styles
        self.configure_styles()
        
        # Créer les widgets
        self.create_widgets()
        
        # Charger les données initiales
        self.load_products()
    
    def configure_styles(self):
        """Configurer les styles pour une interface moderne"""
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Arial", 18, "bold"), foreground="#2c3e50")
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("Danger.TLabel", foreground="red", font=("Arial", 10, "italic"))
        style.configure("Success.TButton", background="#27ae60", foreground="white")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#34495e", foreground="white")
        style.configure("Treeview", rowheight=25)
        style.map("TButton", background=[("active", "#3498db")])

    def create_widgets(self):
        """Créer l'interface utilisateur améliorée"""
        # Header avec bouton retour et titre
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(header_frame, text="← Retour", command=self.return_to_home, style="Success.TButton").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Gestion des Produits", style="Header.TLabel").pack(side=tk.LEFT, padx=20)
        
        # Barre de recherche et filtres
        search_frame = ttk.LabelFrame(self, text="Filtres & Recherche", padding=10)
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(search_frame, text="Rechercher :").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Rechercher", command=self.search_products).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Catégorie :").grid(row=0, column=3, padx=5, pady=5)
        categories = ["Toutes"] + [cat.nom for cat in self.gestion_produit.obtenir_toutes_categories()]
        self.category_combo = ttk.Combobox(search_frame, values=categories, textvariable=self.category_var, width=20, state="readonly")
        self.category_combo.grid(row=0, column=4, padx=5, pady=5)
        self.category_var.set("Toutes")
        ttk.Button(search_frame, text="Filtrer", command=self.filter_products).grid(row=0, column=5, padx=5, pady=5)
        
        # Tableau des produits
        product_frame = ttk.LabelFrame(self, text="Liste des Produits", padding=10)
        product_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        columns = ("id", "reference", "nom", "categorie", "prix_achat", "prix_vente", "stock", "seuil_alerte")
        self.product_tree = ttk.Treeview(product_frame, columns=columns, show="headings", selectmode="browse")
        
        # En-têtes du tableau
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("reference", text="Référence")
        self.product_tree.heading("nom", text="Nom")
        self.product_tree.heading("categorie", text="Catégorie")
        self.product_tree.heading("prix_achat", text="Prix Achat (DA)")
        self.product_tree.heading("prix_vente", text="Prix Vente (DA)")
        self.product_tree.heading("stock", text="Stock")
        self.product_tree.heading("seuil_alerte", text="Seuil Alerte")
        
        # Largeurs des colonnes
        self.product_tree.column("id", width=50, anchor="center")
        self.product_tree.column("reference", width=100)
        self.product_tree.column("nom", width=200)
        self.product_tree.column("categorie", width=100)
        self.product_tree.column("prix_achat", width=100, anchor="e")
        self.product_tree.column("prix_vente", width=100, anchor="e")
        self.product_tree.column("stock", width=80, anchor="center")
        self.product_tree.column("seuil_alerte", width=80, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(product_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Tags pour mise en forme conditionnelle
        self.product_tree.tag_configure("low_stock", background="#f1c40f", foreground="black")
        self.product_tree.tag_configure("critical_stock", background="#e74c3c", foreground="white")
        
        # Menu contextuel
        self.context_menu = tk.Menu(self.product_tree, tearoff=0)
        self.context_menu.add_command(label="Modifier", command=self.edit_product)
        self.context_menu.add_command(label="Supprimer", command=self.delete_product)
        self.context_menu.add_command(label="Ajuster Stock", command=self.adjust_stock)
        self.product_tree.bind("<Button-3>", self.show_context_menu)
        self.product_tree.bind("<Double-1>", lambda event: self.edit_product())
        
        # Boutons d'action
        action_frame = ttk.Frame(self)
        action_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(action_frame, text="Ajouter Produit", command=self.add_product, style="Success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Modifier", command=self.edit_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Supprimer", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Ajuster Stock", command=self.adjust_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Exporter CSV", command=self.export_products).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_frame, text="Produits Faibles", command=self.show_low_stock).pack(side=tk.RIGHT, padx=5)
        
        # Barre de statut
        status_frame = ttk.Frame(self, relief="sunken", borderwidth=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Prêt")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.count_label = ttk.Label(status_frame, text="0 produits")
        self.count_label.pack(side=tk.RIGHT, padx=5)
    
    def load_products(self):
        """Charger tous les produits dans le tableau"""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        products = self.gestion_produit.obtenir_tous_produits()
        for product in products:
            categorie = next((c.nom for c in self.gestion_produit.obtenir_toutes_categories() if c.id == product.categorie_id), "Inconnue")
            tags = []
            if product.quantite <= product.seuil_reapprovisionnement:
                tags.append("low_stock")
            if product.quantite <= product.seuil_reapprovisionnement / 2:
                tags.append("critical_stock")
            
            values = (
                product.id,
                product.nom,  # Note : votre modèle n'a pas de champ "reference", j'utilise "nom" ici
                product.nom,
                categorie,
                f"{product.prix_achat:.2f}",
                f"{product.prix_vente:.2f}",
                product.quantite,
                product.seuil_reapprovisionnement
            )
            self.product_tree.insert("", tk.END, values=values, tags=tags)
        
        self.count_label.config(text=f"{len(products)} produits")
        self.status_label.config(text="Liste des produits chargée")
    
    def search_products(self):
        """Rechercher des produits"""
        term = self.search_var.get().strip().lower()
        if not term:
            self.load_products()
            return
        
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        products = self.gestion_produit.rechercher_produits(term)
        for product in products:
            categorie = next((c.nom for c in self.gestion_produit.obtenir_toutes_categories() if c.id == product.categorie_id), "Inconnue")
            values = (
                product.id,
                product.nom,
                product.nom,
                categorie,
                f"{product.prix_achat:.2f}",
                f"{product.prix_vente:.2f}",
                product.quantite,
                product.seuil_reapprovisionnement
            )
            self.product_tree.insert("", tk.END, values=values)
        
        self.count_label.config(text=f"{len(products)} produits trouvés")
        self.status_label.config(text=f"Recherche: '{term}'")
    
    def filter_products(self):
        """Filtrer par catégorie"""
        category_name = self.category_var.get()
        if category_name == "Toutes":
            self.load_products()
            return
        
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        categorie = next((c for c in self.gestion_produit.obtenir_toutes_categories() if c.nom == category_name), None)
        if categorie:
            products = self.gestion_produit.obtenir_produits_par_categorie(categorie.id)
            for product in products:
                values = (
                    product.id,
                    product.nom,
                    product.nom,
                    category_name,
                    f"{product.prix_achat:.2f}",
                    f"{product.prix_vente:.2f}",
                    product.quantite,
                    product.seuil_reapprovisionnement
                )
                self.product_tree.insert("", tk.END, values=values)
            self.count_label.config(text=f"{len(products)} produits")
            self.status_label.config(text=f"Filtré par catégorie: '{category_name}'")
    
    def show_context_menu(self, event):
        """Afficher le menu contextuel"""
        item = self.product_tree.identify_row(event.y)
        if item:
            self.product_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def add_product(self):
        """Ajouter un produit"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Ajouter un Produit")
        dialog.geometry("500x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        fields = [
            ("Nom", tk.StringVar(), True),
            ("Description", tk.StringVar(), False),
            ("Catégorie", tk.StringVar(), True),
            ("Prix Achat (DA)", tk.DoubleVar(), True),
            ("Prix Vente (DA)", tk.DoubleVar(), True),
            ("Stock Initial", tk.IntVar(), True),
            ("Seuil Alerte", tk.IntVar(), True),
        ]
        
        entries = {}
        for i, (label, var, required) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}{' *' if required else ''} :").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label == "Catégorie":
                categories = [cat.nom for cat in self.gestion_produit.obtenir_toutes_categories()]
                entry = ttk.Combobox(dialog, textvariable=var, values=categories, state="readonly")
            else:
                entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[label] = (entry, var, required)
        
        def save():
            data = {label: var.get() for label, (_, var, _) in entries.items()}
            try:
                categorie_id = next(c.id for c in self.gestion_produit.obtenir_toutes_categories() if c.nom == data["Catégorie"])
                success, produit_id, msg = self.gestion_produit.ajouter_produit(
                    nom=data["Nom"],
                    description=data["Description"],
                    categorie_id=categorie_id,
                    prix_achat=data["Prix Achat (DA)"],
                    prix_vente=data["Prix Vente (DA)"],
                    quantite=data["Stock Initial"],
                    seuil_reapprovisionnement=data["Seuil Alerte"]
                )
                if success:
                    messagebox.showinfo("Succès", msg)
                    dialog.destroy()
                    self.load_products()
                else:
                    messagebox.showerror("Erreur", msg)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de saisie: {e}")
        
        ttk.Button(dialog, text="Enregistrer", command=save, style="Success.TButton").grid(row=len(fields), column=0, pady=20)
        ttk.Button(dialog, text="Annuler", command=dialog.destroy).grid(row=len(fields), column=1, pady=20)
    
    def edit_product(self):
        """Modifier un produit"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Sélectionnez un produit à modifier.")
            return
        
        item = self.product_tree.item(selected[0])
        product_id = item["values"][0]
        product = self.gestion_produit.obtenir_produit_par_id(product_id)
        
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Modifier: {product.nom}")
        dialog.geometry("500x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        fields = [
            ("Nom", tk.StringVar(value=product.nom), True),
            ("Description", tk.StringVar(value=product.description), False),
            ("Catégorie", tk.StringVar(value=next(c.nom for c in self.gestion_produit.obtenir_toutes_categories() if c.id == product.categorie_id)), True),
            ("Prix Achat (DA)", tk.DoubleVar(value=product.prix_achat), True),
            ("Prix Vente (DA)", tk.DoubleVar(value=product.prix_vente), True),
            ("Stock Initial", tk.IntVar(value=product.quantite), True),
            ("Seuil Alerte", tk.IntVar(value=product.seuil_reapprovisionnement), True),
        ]
        
        entries = {}
        for i, (label, var, required) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}{' *' if required else ''} :").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label == "Catégorie":
                categories = [cat.nom for cat in self.gestion_produit.obtenir_toutes_categories()]
                entry = ttk.Combobox(dialog, textvariable=var, values=categories, state="readonly")
            else:
                entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            entries[label] = (entry, var, required)
        
        def update():
            data = {label: var.get() for label, (_, var, _) in entries.items()}
            try:
                categorie_id = next(c.id for c in self.gestion_produit.obtenir_toutes_categories() if c.nom == data["Catégorie"])
                success, _, msg = self.gestion_produit.modifier_produit(
                    id=product_id,
                    nom=data["Nom"],
                    description=data["Description"],
                    categorie_id=categorie_id,
                    prix_achat=data["Prix Achat (DA)"],
                    prix_vente=data["Prix Vente (DA)"],
                    quantite=data["Stock Initial"],
                    seuil_reapprovisionnement=data["Seuil Alerte"]
                )
                if success:
                    messagebox.showinfo("Succès", msg)
                    dialog.destroy()
                    self.load_products()
                else:
                    messagebox.showerror("Erreur", msg)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur de saisie: {e}")
        
        ttk.Button(dialog, text="Mettre à jour", command=update, style="Success.TButton").grid(row=len(fields), column=0, pady=20)
        ttk.Button(dialog, text="Annuler", command=dialog.destroy).grid(row=len(fields), column=1, pady=20)
    
    def delete_product(self):
        """Supprimer un produit"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Sélectionnez un produit à supprimer.")
            return
        
        item = self.product_tree.item(selected[0])
        product_id = item["values"][0]
        product_name = item["values"][2]
        
        if messagebox.askyesno("Confirmer", f"Supprimer '{product_name}' ?"):
            success, msg = self.gestion_produit.supprimer_produit(product_id)
            if success:
                self.load_products()
                self.status_label.config(text=msg)
            else:
                messagebox.showerror("Erreur", msg)
    
    def adjust_stock(self):
        """Ajuster le stock"""
        selected = self.product_tree.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Sélectionnez un produit pour ajuster le stock.")
            return
        
        item = self.product_tree.item(selected[0])
        product_id = item["values"][0]
        product_name = item["values"][2]
        current_stock = item["values"][6]
        
        adjustment = simpledialog.askinteger("Ajuster Stock", 
                                            f"Stock actuel de '{product_name}': {current_stock}\n"
                                            "Quantité à ajouter (positif) ou retirer (négatif):",
                                            parent=self.parent)
        if adjustment is not None:
            success, msg = self.gestion_produit.mettre_a_jour_stock(product_id, adjustment)
            if success:
                self.load_products()
                self.status_label.config(text=msg)
            else:
                messagebox.showerror("Erreur", msg)
    
    def show_low_stock(self):
        """Afficher les produits en faible stock"""
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        products = self.gestion_produit.obtenir_produits_faible_stock()
        for product in products:
            categorie = next((c.nom for c in self.gestion_produit.obtenir_toutes_categories() if c.id == product.categorie_id), "Inconnue")
            values = (
                product.id,
                product.nom,
                product.nom,
                categorie,
                f"{product.prix_achat:.2f}",
                f"{product.prix_vente:.2f}",
                product.quantite,
                product.seuil_reapprovisionnement
            )
            self.product_tree.insert("", tk.END, values=values, tags=("low_stock",))
        
        self.count_label.config(text=f"{len(products)} produits en faible stock")
        self.status_label.config(text="Affichage des produits en faible stock")
    
    def export_products(self):
        """Exporter les produits en CSV"""
        import csv
        products = self.gestion_produit.obtenir_tous_produits()
        with open(f"export_produits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nom", "Catégorie", "Prix Achat", "Prix Vente", "Stock", "Seuil Alerte"])
            for p in products:
                categorie = next((c.nom for c in self.gestion_produit.obtenir_toutes_categories() if c.id == p.categorie_id), "Inconnue")
                writer.writerow([p.id, p.nom, categorie, p.prix_achat, p.prix_vente, p.quantite, p.seuil_reapprovisionnement])
        self.status_label.config(text="Produits exportés en CSV")
    
    def return_to_home(self):
        """Retourner à l'accueil"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        from views.accueil import AccueilView
        AccueilView(self.parent)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion de Magasin - Produits")
    root.geometry("1024x768")
    app = ProduitsView(root)
    root.mainloop()