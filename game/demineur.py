from random import randint
from tkinter import *
import pygame

score = 0
GameOver = False

def créer_terrainMiné(t, taille):
    for i in range(taille):
        ligne = []
        for j in range(taille):
            ligne.append(0)
        t.append(ligne)
    print(t)


def pose_mine(t, x):
    for i in range(x):
        a = randint(0, 7)
        b = randint(0, 7)
        t[a][b] = 1

def affichage_ecran(event, t, i, j, score_points):
    global score
    global GameOver

    carré = event.widget
    texte_basique = carré.cget("text")

    if GameOver is False and texte_basique == "":
        bombes_voisines = 0
        for x in range(max(0, i-1), min(8, i+2)):
            for y in range(max(0, j-1), min(8, j+2)):
                bombes_voisines += t[x][y]

        carré.config(bg="saddlebrown", text=str(bombes_voisines))

        score = score + 1
        score_points.config(text="Score : {}".format(score))

        if t[i][j] == 1:
            GameOver = True
            carré.config(bg="red")
            print("GAME OVER ! Tu as touché une bombe !")
            print("Ton score :", score)



pygame.init() 
pygame.mixer.init

def jouer_musique():
    pygame.mixer.music.load("C:/Users/Utilisateur/Desktop/Programmation/Projet_Ecole/demineur/son_demineur.wav")
    pygame.mixer.music.play(loops=0)

def configuration_fenêtre(fenêtre, t, score_points, taille):
    for i in range(taille):
        for j in range(taille):
            bouton = Button(fenêtre, width=5, height=2, bg='green', command=jouer_musique)
            bouton.grid(row=i, column=j)
            bouton.bind("<Button-1>", lambda event, t=t, i=i, j=j: affichage_ecran(event, t, i, j, score_points))

def jouer_démineur(mode, taille, mines):
    terrainMiné = []
    créer_terrainMiné(terrainMiné, taille)
    pose_mine(terrainMiné, mines) 

    fenêtre = Tk()
    fenêtre.title("Démineur [MODE {}]".format(mode))
    score_points = Label(fenêtre, text="Score : {}".format(score))
    score_points.grid(row=taille, column=0, columnspan=taille)

    def fermer_fenetre():
        fenêtre.destroy()

    fenêtre.protocol("WM_DELETE_WINDOW", fermer_fenetre)
    configuration_fenêtre(fenêtre, terrainMiné, score_points, taille)
    fenêtre.mainloop()

def jouer_mode_facile():
    accueil.destroy()
    jouer_démineur("DEBUTANT", 8, 8)

def jouer_mode_moyen():
    accueil.destroy()
    jouer_démineur("PRO", 12, 12)

def jouer_mode_difficile():
    accueil.destroy()
    jouer_démineur("HACKER", 16, 16)


accueil = Tk()
accueil.title("PAGE D'ACCUEIL DEMINEUR")
accueil.configure(bg="gray")
accueil.minsize(500, 500)

photo = PhotoImage(file="demineur.png")
photo = photo.subsample(5, 5)  

canvas = Canvas(accueil, width=photo.width(), height=photo.height(), bg='white')
canvas.place(x=50, y=50)

canvas.create_image(0, 0, anchor=NW, image=photo)

bouton_accueil_facile = Button(accueil, text="DEBUTANT", width=10, height=5, bg='green', command=jouer_mode_facile)
bouton_accueil_facile.place(x=110, y=400)

bouton_accueil_moyen = Button(accueil, text="PRO", width=10, height=5, bg='orange', command=jouer_mode_moyen)
bouton_accueil_moyen.place(x=210, y=400)

bouton_accueil_difficile = Button(accueil, text="HACKER", width=10, height=5, bg='red', command=jouer_mode_difficile)
bouton_accueil_difficile.place(x=310, y=400)

accueil.mainloop()
