# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:09:00 2019

@author: axelg
"""

from random import randint
import tkinter as tk

class Tetris:
    def __init__(self):
        self.hauteur = 22
        self.largeur = 10
        self.taille_case = 20
        self.width, self.height= self.largeur*self.taille_case, self.hauteur*self.taille_case
        self.Canvas = tk.Canvas(fenetre, width = self.width, height = self.height, bg = "white")
       
        self.grille = [[0 for i in range(self.largeur)] for y in range(self.hauteur)]

        self.pieces = [[[[1, 1],            # O
                         [1, 1]]],
                       
                       [[[2, 2, 2],         # T:1
                         [0, 2, 0]],
                        [[0, 2],            # T:2
                         [2, 2],
                         [0, 2]],
                        [[0, 2, 0],         # T:3
                         [2, 2, 2]],
                        [[2, 0],            # T:4
                         [2, 2],
                         [2, 0]]],
                       [[[3,3,3,3]],        # I:0
                        [[3],               # I:1
                         [3],
                         [3],
                         [3]]],
                       [[[4,4,4],           # L:0
                         [4,0,0]],
                        [[4,4],              # L:1
                         [0,4],
                         [0,4]],
                        [[0,0,4],           # L:2
                         [4,4,4]],
                        [[4,0],             # L:3
                         [4,0],
                         [4,4]]],
                       [[[5,5,5],           # J:0
                         [0,0,5]],
                        [[0,5],              # J:1
                         [0,5],
                         [5,5]],
                        [[5,0,0],           # J:2
                         [5,5,5]],
                        [[5,5],             # J:3
                         [5,0],
                         [5,0]]],
                       [[[6,6,0],           # Z:0
                         [0,6,6]],
                        [[0,6],              # Z:1
                         [6,6],
                         [6,0]]],
                       [[[0,7,7],           # S:0
                         [7,7,0]],
                        [[7,0],              # S:1
                         [7,7],
                         [0,7]]],
                       [[[1,2],
                         [3,4]]],
                       [[[4,0,4,4,4],
                         [4,0,4,0,0],
                         [4,4,4,4,4],
                         [0,0,4,0,4],
                         [4,4,4,0,4]]],
                         [[[0,0,8,8,0,0,8,0,0],
                           [0,8,8,8,0,0,0,8,0],
                           [8,8,8,0,0,0,0,0,8],
                           [8,8,0,8,0,0,0,0,8],
                           [0,0,0,0,8,0,0,8,0],
                           [0,0,0,0,0,8,0,8,0],
                           [0,0,8,0,0,8,8,0,0],
                           [0,8,0,8,8,0,0,8,0],
                           [8,0,0,0,0,0,0,0,8]]]] 
        
        self.current_piece = [] #Donne les information de la piece en cours : current_piece[0]: piece, current_piece[1] : configuration de la piece
        self.spawn_piece()

        fenetre.bind('<KeyPress>', self.keypressed)
        self.Canvas.pack()
       
        self.dessiner_grille()
        self.dessiner_piece()
        self.down_piece()


    def keypressed(self, event):
        self.clear_piece()

        mvt = [0,0] #definit le mouvement en x et y
        turn = False #la piece a tourner ?

        if event.keysym == "Right":
            mvt[0] = 1
        if event.keysym == "Left":
            mvt[0] = -1               
        if event.keysym == "Down":
             mvt[1] = -1
             
        if event.keysym == "Up":
            turn = True
            self.tourner_piece(True)

        self.pos_piece[0] += mvt[0]
        self.pos_piece[1] += mvt[1]

        if self.collision_murs():
            self.pos_piece[0] -= mvt[0]

        if self.collision_piece():
            if turn:
                self.tourner_piece(False)
            else:
                self.pos_piece[0] -= mvt[0]
                self.pos_piece[1] -= mvt[1]
                if not (mvt[0] == 1 or mvt[0] == -1 and mvt[1] == 0):   #permet aux pieces de glisser verticalement contre des pieces deja posées
                    self.dessiner_piece()
                    self.add_to_grille()
                    self.spawn_piece()

                

        if self.collision_sol():
            self.pos_piece[1] -= mvt[1]
            self.dessiner_piece()

            self.add_to_grille()
            self.spawn_piece()
        self.dessiner_piece()
       
    
    def down_piece(self):
        #TODO : faire le check des collisions.
        self.clear_piece()
        self.pos_piece[1] -= 1
        if self.collision_piece():
            self.pos_piece[1] += 1
            self.dessiner_piece()
            self.add_to_grille()
            self.spawn_piece()

        if self.collision_sol():
            self.pos_piece[1] += 1
            self.dessiner_piece()
            self.add_to_grille()
            self.spawn_piece()

        self.dessiner_piece()
        self.Canvas.after(1000, self.down_piece)

    def spawn_piece(self):
        self.pos_piece = [4, self.hauteur+1]
        self.current_piece = [randint(0,6), 0]

        
    def tourner_piece(self, clockwise):
        N = len(self.pieces[self.current_piece[0]])
        self.current_piece[1]  += (-1, 1)[clockwise]
        if self.current_piece[1] == N:
            self.current_piece[1] = 0
        elif self.current_piece[1] == -1:
            self.current_piece[1] = N-1
        
    #Check de collision avec le sol. [move D]
    def collision_sol(self):
        if self.pos_piece[1] == -1:
            return True
        return False

    #Check de la collision de la piece avec l'un des deux murs. [move R/L]
    def collision_murs(self):
        n, c = self.current_piece[0], self.current_piece[1]
        for i in range(len(self.pieces[n][c])):
            if self.pos_piece[0] == -1 or self.pos_piece[0]+ len(self.pieces[n][c][i])-1 == self.largeur:
                return True
        return False
        
    #Check de la collision de la piece avec des blocs deja dans la grille. [move R/L/D/Spawn]
    def collision_piece(self):
        n, c = self.current_piece[0], self.current_piece[1]
        for i in range(len(self.pieces[n][c])):
            for j in range(len(self.pieces[n][c][i])):
                if self.pos_piece[1]+(len(self.pieces[n][c])-i-1) < self.hauteur and self.pos_piece[0]+j < self.largeur:
                    a = self.grille[self.pos_piece[1]+(len(self.pieces[n][c])-i-1)][self.pos_piece[0]+j]
                    if not a == 0 and not self.pieces[n][c][i][j] == 0:
                        return True
        return False

    def add_to_grille(self):
        n, c = self.current_piece[0], self.current_piece[1]
        for i in range(len(self.pieces[n][c])):
            for j in range(len(self.pieces[n][c][i])):
                    if not self.pieces[n][c][i][j] == 0 and self.pos_piece[1]+(len(self.pieces[n][c])-i-1) < self.hauteur:
                        self.grille[self.pos_piece[1]+(len(self.pieces[n][c])-i-1)][self.pos_piece[0]+j] = self.pieces[n][c][i][j]
        
    def dessiner_piece(self):
        n, c = self.current_piece[0], self.current_piece[1]
        for i in range(len(self.pieces[n][c])):
            for j in range(len(self.pieces[n][c][i])):
                if not self.pieces[n][c][i][j] == 0:
                    self.dessiner_case(self.pos_piece[0]*self.taille_case + j*self.taille_case, (self.hauteur-self.pos_piece[1])*self.taille_case +(-len(self.pieces[n][c]) + i)*self.taille_case , self.choix_couleur(self.pieces[n][c][i][j]))

    def clear_piece(self):
        n, c = self.current_piece[0], self.current_piece[1]
        for i in range(len(self.pieces[n][c])):
            for j in range(len(self.pieces[n][c][i])):
                if self.pos_piece[1]+(len(self.pieces[n][c])-i-1) < self.hauteur and self.pos_piece[0]+j < self.largeur:
                    a = self.grille[self.pos_piece[1]+(len(self.pieces[n][c])-i-1)][self.pos_piece[0]+j]
                    if a == 0:
                        self.dessiner_case(self.pos_piece[0]*self.taille_case + j*self.taille_case, (self.hauteur-self.pos_piece[1])*self.taille_case +(-len(self.pieces[n][c]) + i)*self.taille_case , "white")


    def dessiner_grille(self):
        for i in range(self.hauteur):
            for j in range(self.largeur):
                x = self.pos(j, i)
                self.dessiner_case(x[0], x[1], self.choix_couleur(self.grille[i][j]))

    def dessiner_case(self, i, j, color):
        self.carre = self.Canvas.create_rectangle(i, j, i + self.taille_case,j+self.taille_case, fill = color)

    def choix_couleur(self, n):
        if n == 0:
            return "white"
        elif n == 1:
            return "yellow"
        elif n == 2:
            return "purple"
        elif n == 3:
            return "#47cef7"
        elif n == 4:
            return "#ea9012"
        elif n == 5:
            return '#1324db'
        elif n == 6:
            return '#ef0707'
        elif n == 7:
            return '#1bc607'
        elif n == 8:
            return '#ffdd00'

    def pos(self, i, j):
        return [i*self.taille_case, (self.hauteur-j)*self.taille_case - self.taille_case]

fenetre = tk.Tk()
App = Tetris()
fenetre.mainloop()