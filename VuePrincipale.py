# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import tkinter as tk
from PIL import Image, ImageTk


class VuePrincipale(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("smooth attaque")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # Widgets
        self.creer_widgets()

    def creer_widgets(self):

        self.nom = tk.Label(self, text="Smooth attaque", bg = 'lightblue', font=("Algerian", 50))
        self.nom.grid(row = 0, column = 50, columnspan=200)
        
        # Bouton lancr le jeu
        self.bouton_lancer_jeu = tk.Button(self, text="Lancer le jeu", font=("Calibri", 20))
        #self.bouton_lancer_jeu.bind('<Button-1>', self.lancer_jeu)
        self.bouton_lancer_jeu.grid(row=12, column=100, rowspan=10)
        
        # Bouton quitter
        self.bouton_quitter = tk.Button(self, text="quitter l'application")
        self.bouton_quitter.bind("<Button-1>",self.quitter)
        self.bouton_quitter.grid(row=40, column=100)
        
        #image de fruits
        #photo = tk.PhotoImage(file="pasteque.jpg")
        #label = tk.Label(self, image=photo)
        #label.image = photo  # IMPORTANT : garder une référence sinon l'image disparaît
        #label.grid(row = 15, column = 2)

    def quitter(self,event):
        self.destroy()
            

        
        
app = VuePrincipale()
app.mainloop()