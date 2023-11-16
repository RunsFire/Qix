from fltk import *




largeurFenetre = 1000           # à modifier pour que
hauteurFenetre = 900            # la résolution change




def carre(x, y, cote, coul, remplir, nom, taille) :
    """Dessine un carré avec x et y comme coordonnées d'un coin et cote comme longueur."""
    rectangle(x, y, x + cote, y + cote, couleur=coul, remplissage=remplir, tag=nom, epaisseur=taille)






def ecran_launch() :
    """Crée le menu de départ."""
    coin_sup_gauche = [200,175]
    coin_inf_droite = [800,850]
    cree_fenetre(largeurFenetre, hauteurFenetre)
    rectangle(0,0,largeurFenetre, hauteurFenetre, remplissage = "black")
    carre(400,405,200,"White",None,"carre","10")
    rectangle(coin_sup_gauche[0], coin_sup_gauche[1], coin_inf_droite[0], coin_inf_droite[1], "white", tag="ZdJ")
    texte(500, 500, "QIX", "white", "center", "Reem Kufi", 50)
    attend_clic_gauche()
    rectangle(350,350,650,650, "black", remplissage="black")
    texte(500, 500, "Appuyez sur click \ngauche pour jouer", "gray", "center", "Arial", 30)
    attend_clic_gauche()
    rectangle(300,300,700,700, "black", remplissage="black")
    texte(500, 87.5, "QIX", "Light Gray", "center", "Reem Kufi", 60)
    rectangle(405,50,600,140, "Gray", epaisseur="8")
    rectangle(405,50,600,140, "Gold", epaisseur="2")
    return coin_sup_gauche, coin_inf_droite




def affichage_perdu(nbVies) :
    """Affiche le message de perte avec nbVies le nombre de vies restantes du joueur."""
    texte(largeurFenetre / 2, hauteurFenetre / 2, "Perdu", "Red", "center", taille = 25, tag = "Perdu")
    texte(largeurFenetre / 2, hauteurFenetre * 3 / 4, "Appuyez sur click gauche pour continuer", "white", "center", taille = 10, tag = "Continue")
    mise_a_jour
    attend_clic_gauche()
    efface("Perdu")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Vies restantes :", "Red", "center", taille = 25, tag = "Restes")
    texte(largeurFenetre / 2, hauteurFenetre / 2, nbVies, "Red", "center", taille = 25, tag = "nbVies")
    mise_a_jour
    attend_clic_gauche()
    efface("nbVies")
    efface("Restes")
    efface("Trainée")
    efface("Continue")
    mise_a_jour






def affichage_gagne(niveau) :
    """Affiche le message de victoire avec niveau le niveau du jeu."""
    texte(largeurFenetre / 2, hauteurFenetre * 3 / 4, "Appuyez sur click gauche pour continuer", "white", "center", taille = 10, tag = "Continue")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Vous avez gagné", "Red", "center", taille = 25, tag = "Gagner")
    mise_a_jour
    attend_clic_gauche()
    efface("Gagner")
    texte(largeurFenetre / 2, hauteurFenetre / 2 - 30, "Niveau " + str(niveau), "Red", "center", taille = 25, tag = "Niveau")
    mise_a_jour
    attend_clic_gauche()
    efface("Niveau")
    efface("Continue")
    mise_a_jour






def curseur(x, y, rayon) :
    """Dessine le joueur (qui est un cercle bleu)"""
    cercle(x, y, rayon, "Aqua",epaisseur='2', tag = "curseur")






def sparx(x,y) :
    '''Dessine le sparx (bordure blanche, remplissage magenta)'''
    cercle(x, y,5,couleur="White",remplissage="Magenta",epaisseur='2',tag="Sparx")