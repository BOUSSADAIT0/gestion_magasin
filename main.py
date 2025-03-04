# main.py - Point d'entrée de l'application

import tkinter as tk
from tkinter import ttk
from views.accueil import AccueilView

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Magasin - Matériaux de Construction")
        self.geometry("1200x700")
        
        # Configuration du style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', background='#4a7abc', foreground='white')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Conteneur principal
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Charger la vue d'accueil
        self.current_view = AccueilView(self.main_container)
        
    def switch_view(self, view_class, *args, **kwargs):
        # Nettoyer la vue actuelle
        if hasattr(self, 'current_view'):
            self.current_view.destroy()
        
        # Charger la nouvelle vue
        self.current_view = view_class(self.main_container, *args, **kwargs)

if __name__ == "__main__":
    from utils.db_setup import setup_database
    
    # Initialiser la base de données
    setup_database()
    
    # Lancer l'application
    app = Application()
    app.mainloop()