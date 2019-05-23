# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:09:00 2019

@author: axelg
"""

from random import randint
import tkinter as tk
import hashlib as hl

        
class Tetris:
    def __init__(self):
        self.hauteur = 22
        self.largeur = 10
        self.taille_case = 28
        self.width, self.height= self.largeur*self.taille_case, self.hauteur*self.taille_case
        self.Canvas = tk.Canvas(fenetre, width = self.width, height = self.height, bg = "white")
        
        self.grille = []
        self.creer_grille()
        self.grille[5][5] = 1
        
        self.dessiner_grille()
        
        self.pieces = [[[[1, 1, 0,0],
                         [1, 1, 0, 0],
                         [0,0,0,0],
                         [0,0,0,0]]]]
    
        self.pos_piece = (0, 0)
        self.dessiner_piece(0);
        self.Canvas.pack()
        
    def creer_grille(self):
        for i in range(self.hauteur):
            self.grille.append([0]*self.largeur)
        print(len(self.grille))
        
    def dessiner_piece(self, n):
        
        for i in range(4):
            for j in range(4):
                if self.pieces[n][0][i][j] == 0:
                    self.dessiner_case2(i, j, "white")
                elif self.pieces[n][0][i][j] == 1:
                    self.dessiner_case2(i, j, "red")
                


    def dessiner_grille(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                if self.grille[i][j] == 0:
                    self.dessiner_case(i, j, "white")
                elif self.grille[i][j] ==1:
                    self.dessiner_case(i, j, "yellow")
                
    def dessiner_case2(self, i, j, color):
        tp = self.taille_case
        self.carre = self.Canvas.create_rectangle(i*tp + self.pos_piece[0], j*tp + self.pos_piece[1], i*tp + self.pos_piece[0] +tp , j*tp + self.pos_piece[1]+tp, fill = color)
    def dessiner_case(self, i, j, color):
        x = self.pos(j, i)
        self.carre = self.Canvas.create_rectangle(x[0], x[1], x[0]+ 28,x[1]- 28, fill = color)
    
    def pos(self, i, j):
        return [i*self.taille_case, self.height-j*self.taille_case]
        
        
fenetre = tk.Tk()
App = Tetris()
fenetre.mainloop()