from fltk import *
import os
from Gameplay import zonetot, zone_a_capture, nbVies, niveau, score



largeurFenetre = 1000           # à modifier pour que
hauteurFenetre = 900            # la résolution change
path = os.getcwd()



def carre(x, y, cote, coul, remplir, nom, taille) :
    """Dessine un carré avec x et y comme coordonnées d'un coin et cote comme longueur."""
    rectangle(x, y, x + cote, y + cote, couleur=coul, remplissage=remplir, tag=nom, epaisseur=taille)





def ecran_launch() :
    """Crée le menu de départ."""
    coin_sup_gauche = [200,180]
    coin_inf_droite = [800,850]
    cree_fenetre(largeurFenetre, hauteurFenetre)
    rectangle(0,0,largeurFenetre, hauteurFenetre, remplissage = "black")        # Fond
    rectangle(coin_sup_gauche[0], coin_sup_gauche[1], coin_inf_droite[0], coin_inf_droite[1], "white", tag="ZdJ")       # Zone de Jeu
    image(largeurFenetre//2,hauteurFenetre//2, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))      # Logo Qix (start)
    rectangle(320,352,680,548, "white", epaisseur="5", tag="im")        # Cadre du logo
    attend_clic_gauche()
    efface("im")
    texte(500, 500, "Appuyez sur click \ngauche pour jouer", "gray", "center", police="Lucida Console",taille=30, tag="interaction")     # Message pour jouer
    attend_clic_gauche()
    efface('interaction')     
    # - = - = - Logo Qix - = - = -
    image(largeurFenetre//2, 87.5,  os.path.join(path,'QIX_logo.gif'), tag="aff", largeur=190, hauteur=int(188*(150/414)))
    rectangle(390,33.5,610,141.5, "Gray", epaisseur="8")
    rectangle(390,33.5,610,141.5, "Gold", epaisseur="2")
    # * - * = * - * = * - * Score * - * = * - * = * - *
    # - = - = - Taux de capture - = - = -
    ligne(186,129,206,95,"gray",epaisseur="2")
    texte(106,113, str(round(zonetot,2)) + " %","white","center", police="Lucida Console",taille=30, tag="Zonecapturee")
    texte(260,113, str(zone_a_capture) + "%","gray","center", police="Lucida Console",taille=30, tag="Zone_a_capturee")
    # - = - = - Vies - = - = - 
    texte(670,114, str(nbVies), "Violet", "center", police="Lucida Console", taille = 25, tag = "nbVies")
    image(700,113, os.path.join(path,'heart.gif'), ancrage="center",tag="im")
    # - = - = - Niveau - = - = -
    texte(775,55, "Niveau :","light gray","center", police="Lucida Console",taille=30)
    texte(900,55,str(niveau),"light gray","center", police="Lucida Console",taille=30, tag="niveau")
    # - = - = - Indications - = - = -
    texte(850,113,"Drawing","red","center", police="Courier",taille=20, tag="dessiner")
    # - = - = - Score - = - = - 
    texte(106,50, "Score :","white","center", police="Lucida Console",taille=30)
    texte(275,50, str(score),"white","center", police="Lucida Console",taille=30, tag="score")
    return coin_sup_gauche, coin_inf_droite



def update_act(zonetot,score):
    '''Mettre à jour les différentes informations qui doivent l'être après chaque action.'''
    texte(106,113, str(round(zonetot,2)) + "%","white","center", police="Lucida Console",taille=30, tag="Zonecapturee")
    texte(275,50, str(score),"white","center", police="Lucida Console",taille=30, tag="score")

def update_round(zone_a_capture, nbVies,niveau):
    '''Mettre à jour les différentes informations qui doivent l'être après chaque niveau.'''
    texte(260,113, str(zone_a_capture) + "%","gray","center", police="Lucida Console",taille=30, tag="Zone_a_capturee")
    texte(670,114, str(nbVies), "Violet", "center", police="Liberation Mono",taille=25, tag = "nbVies")
    texte(900,55,str(niveau),"light gray","center", police="Liberation Mono",taille=30, tag="niveau")
    draw(0)

def draw(spd):
    efface("dessiner")
    if spd == 0:
        texte(850,113,"Drawing","red","center", police="Lucida Console",taille=20, tag="dessiner")
    elif spd == 1 :
        texte(850,113,"Drawing","green","center", police="Lucida Console",taille=20, tag="dessiner")
    else :
        texte(850,113,"Drawing","blue","center", police="Lucida Console",taille=20, tag="dessiner")

    




def affichage_perdu(nbVies) :
    """Affiche le message de perte avec nbVies le nombre de vies restantes du joueur."""
    texte(largeurFenetre / 2, hauteurFenetre / 2, "Perdu", "Red", "center", police="Lucida Console", taille = 25, tag = "Perdu")
    texte(largeurFenetre / 2, hauteurFenetre * 3 / 4, "Appuyez sur click gauche pour continuer", "white", "center", police="Lucida Console", taille = 10, tag = "Continue")
    mise_a_jour()
    attend_clic_gauche()
    efface("Perdu")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Vies restantes :", "Red", "center", police="Lucida Console", taille = 25, tag = "Restes")
    texte(largeurFenetre / 2, hauteurFenetre / 2, nbVies, "Red", "center", police="Lucida Console", taille = 25, tag = "nbVies")
    mise_a_jour()
    attend_clic_gauche()
    efface("nbVies")
    efface("Restes")
    efface("Trainée")
    efface("Continue")
    mise_a_jour()





def affichage_gagne(niveau) :
    """Affiche le message de victoire avec niveau le niveau du jeu."""
    texte(largeurFenetre / 2, hauteurFenetre * 3 / 4, "Appuyez sur click gauche pour continuer", "white", "center", police="Lucida Console", taille = 10, tag = "Continue")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Vous avez gagné", "Red", "center", police="Lucida Console", taille = 25, tag = "Gagner")
    mise_a_jour()
    attend_clic_gauche()
    efface("Gagner")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Niveau " + str(niveau), "Red", "center", police="Lucida Console", taille = 25, tag = "Niveau")
    mise_a_jour()
    attend_clic_gauche()
    efface("Niveau")
    efface("Continue")
    mise_a_jour()





def curseur(x, y, rayon) :
    """Dessine le joueur (qui est un cercle bleu)"""
    cercle(x, y, rayon, "Aqua",epaisseur='2', tag = "curseur")





def sparx(x,y) :
    '''Dessine le sparx (bordure blanche, remplissage magenta)'''
    cercle(x, y,5,couleur="White",remplissage="Magenta",epaisseur='2',tag="Sparx")