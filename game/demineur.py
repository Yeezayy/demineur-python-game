import os
from random import randint
from tkinter import *
import pygame
from tkinter import PhotoImage

score = 0
GameOver = False


def creer_terrainMine(t, taille):
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


pygame.init()
pygame.mixer.init

def jouer_musique():
    current_dir = os.path.dirname(__file__)
    chemin_son = os.path.join(current_dir, "assets", "explosion.mp3")
    
    pygame.mixer.music.load(chemin_son)
    pygame.mixer.music.play(loops=0)


def reveler_cases_adjacent(t, boutons, i, j, taille):
    pile = [(i, j)]
    visites = set()

    while pile:
        x, y = pile.pop()

        if (x, y) in visites:
            continue
        visites.add((x, y))

        bombes_voisines = 0
        for voisin_x in range(max(0, x - 1), min(taille, x + 2)):
            for voisin_y in range(max(0, y - 1), min(taille, y + 2)):
                bombes_voisines += t[voisin_x][voisin_y]

        bouton = boutons[x][y]

        if bouton.cget("text") == "": 
            bouton.config(bg="saddlebrown", text=str(bombes_voisines) if bombes_voisines > 0 else "")

        if bombes_voisines == 0:
            for voisin_x in range(max(0, x - 1), min(taille, x + 2)):
                for voisin_y in range(max(0, y - 1), min(taille, y + 2)):
                    if (voisin_x, voisin_y) != visites:
                        pile.append((voisin_x, voisin_y))


def affichage_ecran(event, t, boutons, i, j, score_points, taille):
    global score
    global GameOver

    carre = event.widget
    texte_basique = carre.cget("text")

    if GameOver is False and texte_basique == "":
        bombes_voisines = 0
        for x in range(max(0, i - 1), min(taille, i + 2)):
            for y in range(max(0, j - 1), min(taille, j + 2)):
                bombes_voisines += t[x][y]

        if t[i][j] == 1:
            GameOver = True
            carre.config(bg="red")
            jouer_musique()
            print("GAME OVER ! Tu as touché une bombe !")
            print("Ton score :", score)
        else:
            reveler_cases_adjacent(t, boutons, i, j, taille)
            score += 1
            score_points.config(text="Score : {}".format(score))


def configuration_fenetre(fenetre, t, score_points, taille):
    boutons = []
    for i in range(taille):
        ligne_boutons = []
        for j in range(taille):
            bouton = Button(fenetre, width=5, height=2, bg='green')
            bouton.grid(row=i, column=j)
            bouton.bind("<Button-1>", lambda event, t=t, i=i, j=j: affichage_ecran(event, t, boutons, i, j, score_points, taille))
            ligne_boutons.append(bouton)
        boutons.append(ligne_boutons)


def jouer_demineur(mode, taille, mines):
    terrainMine = []
    creer_terrainMine(terrainMine, taille)
    pose_mine(terrainMine, mines)

    fenetre = Tk()
    fenetre.title("Démineur [MODE {}]".format(mode))
    score_points = Label(fenetre, text="Score : {}".format(score))
    score_points.grid(row=taille, column=0, columnspan=taille)

    def fermer_fenetre():
        fenetre.destroy()

    fenetre.protocol("WM_DELETE_WINDOW", fermer_fenetre)
    configuration_fenetre(fenetre, terrainMine, score_points, taille)
    fenetre.mainloop()


def jouer_mode_facile():
    accueil.destroy()
    jouer_demineur("DEBUTANT", 8, 8)


def jouer_mode_moyen():
    accueil.destroy()
    jouer_demineur("PRO", 12, 12)


def jouer_mode_difficile():
    accueil.destroy()
    jouer_demineur("HACKER", 16, 16)


accueil = Tk()
accueil.title("PAGE D'ACCUEIL DEMINEUR")
accueil.configure(bg="gray")
accueil.minsize(500, 500)

current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "assets", "demineur.png")

photo = PhotoImage(file=image_path)
photo = photo.subsample(4, 4)

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
