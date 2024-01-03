from fltk import *
import os
import string


largeurFenetre = 1000           # à modifier pour que
hauteurFenetre = 900            # la résolution change
path = os.getcwd()



def carre(x: int, y: int, cote: int, coul="black", remplir=None, nom=None, taille=1.0) -> None :
    """Dessine un carré avec x et y comme coordonnées d'un coin et cote comme longueur.
    :param int x: abs du premier coin
    :param int y: ord du premier coin
    :param int cote: longueur du coté du carré
    :param str coul: couleur du contour du carré (défaut "black")
    :param str remplir: couleur du remplissage du carré (défaut "transparent")
    :param str nom: tag du carré (défaut "None")
    :param float taille: epaisseur du contour (défaut "1")"""
    rectangle(x, y, x + cote, y + cote, couleur=coul, remplissage=remplir, tag=nom, epaisseur=taille)





def ecran_launch(zonetot: float, zone_a_capture: float, nbVies: int, niveau: int, score: int) -> tuple :
    """Crée le menu de départ."""
    coin_sup_gauche = [200,180]
    coin_inf_droite = [800,850]
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
    if score != None :
        texte(106,50, "Score :","white","center", police="Lucida Console",taille=30)
        texte(275,50, str(score),"white","center", police="Lucida Console",taille=30, tag="score")
    return coin_sup_gauche, coin_inf_droite



def update_act(zonetot: float, score: int) -> None:
    '''Mettre à jour les différentes informations qui doivent l'être après chaque action.'''
    texte(106,113, str(round(zonetot,2)) + "%","white","center", police="Lucida Console",taille=30, tag="Zonecapturee")
    if score != None :
        texte(275,50, str(score),"white","center", police="Lucida Console",taille=30, tag="score")

def update_round(zone_a_capture: int, nbVies: int, niveau: int) -> None:
    '''Mettre à jour les différentes informations qui doivent l'être après chaque niveau.'''
    texte(260,113, str(zone_a_capture) + "%","gray","center", police="Lucida Console",taille=30, tag="Zone_a_capturee")
    texte(670,114, str(nbVies), "Violet", "center", police="Liberation Mono",taille=25, tag = "nbVies")
    texte(900,55,str(niveau),"light gray","center", police="Liberation Mono",taille=30, tag="niveau")
    draw(0)

def draw(spd: int) -> None:
    efface("dessiner")
    if spd == 0:
        texte(850,113,"Drawing","red","center", police="Lucida Console",taille=20, tag="dessiner")
    elif spd == 1 :
        texte(850,113,"Drawing","green","center", police="Lucida Console",taille=20, tag="dessiner")
    else :
        texte(850,113,"Drawing","blue","center", police="Lucida Console",taille=20, tag="dessiner")

    




def affichage_perdu(nbVies: int) -> None :
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





def affichage_gagne(niveau: int) -> None :
    """Affiche le message de victoire avec le niveau du jeu."""
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





def curseur(x: int, y: int, rayon: int) -> None :
    """Dessine le joueur (qui est un cercle bleu)"""
    cercle(x, y, rayon, "Aqua",epaisseur='2', tag = "curseur")





def sparx(x: int, y: int) -> None :
    '''Dessine le sparx (bordure blanche, remplissage magenta)'''
    cercle(x, y, 5,couleur="White",remplissage="Magenta",epaisseur='2',tag="Sparx")


def menu_principal(largeurFenetre: int, hauteurFenetre: int, path: str) -> str :
    rectangle(0,0, largeurFenetre, hauteurFenetre, "black", "black", 1, "bg")
    image(largeurFenetre // 2, 125, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur= 300, hauteur=int(188*(300/414)))

    rectangle(largeurFenetre // 2 - 200, 250,largeurFenetre // 2 + 200, 300, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 275, "Commencer", "white", "center", taille=24, tag="Commencer")

    rectangle(largeurFenetre // 2 - 200, 325,largeurFenetre // 2 + 200, 375, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 350, "Variantes", "white", "center", taille=24, tag="Variantes")

    rectangle(largeurFenetre // 2 - 200, 400,largeurFenetre // 2 + 200, 450, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 425, "Paramètres", "white", "center", taille=24, tag="Parametres")

    rectangle(largeurFenetre // 2 - 200, 475,largeurFenetre // 2 + 200, 525, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 500, "Quitter", "white", "center", taille=24, tag="Quitter")

    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        if largeurFenetre // 2 - 200 <= x_souris <= largeurFenetre // 2 + 200 :
            if 250 <= y_souris <= 300 :
                rectangle(largeurFenetre // 2 - 200, 250,largeurFenetre // 2 + 200, 300, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Commencer"
            elif 325 <= y_souris <= 375 :
                rectangle(largeurFenetre // 2 - 200, 325,largeurFenetre // 2 + 200, 375, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Variantes"
            elif 400 <= y_souris <= 450 :
                rectangle(largeurFenetre // 2 - 200, 400,largeurFenetre // 2 + 200, 450, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Parametres"
            elif 475 <= y_souris <= 525 :
                rectangle(largeurFenetre // 2 - 200, 475,largeurFenetre // 2 + 200, 525, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    break
        mise_a_jour()
        if tev == "Quitte" :
            break
        elif tev == "Touche" :
            if touche(ev) == 'Escape' :
                rectangle(largeurFenetre // 2 - 200, hauteurFenetre // 2 - 100, largeurFenetre // 2 + 200, hauteurFenetre // 2 + 100, "white", "black", epaisseur=4, tag="confirmer")
                texte(largeurFenetre // 2, hauteurFenetre // 2 - 50, "Êtes-vous sur de", "red", "center", 20, tag="confirmer")
                texte(largeurFenetre // 2, hauteurFenetre // 2 - 10, "vouloir quitter ?", "red", "center", 20, tag="confirmer")

                rectangle(largeurFenetre // 2 - 100, hauteurFenetre // 2 + 80, largeurFenetre // 2 - 40, hauteurFenetre // 2 + 50, "white", "black", 2, tag="confirmer")
                texte(largeurFenetre // 2 - 70, hauteurFenetre // 2 + 65, "Oui", "red", "center", taille=13, tag="oui")

                rectangle(largeurFenetre // 2 + 100, hauteurFenetre // 2 + 80, largeurFenetre // 2 + 40, hauteurFenetre // 2 + 50, "white", "black", 2, tag="confirmer")
                texte(largeurFenetre // 2 + 70, hauteurFenetre // 2 + 65, "Non", "lime", "center", taille=13, tag="non")

                while True :
                    ev = donne_ev()
                    tev = type_ev(ev)
                    x_souris = abscisse_souris()
                    y_souris = ordonnee_souris()
                    efface('cadre')
                    if hauteurFenetre // 2 + 50 <= y_souris <= hauteurFenetre // 2 + 80 :
                        if largeurFenetre // 2 - 100 <= x_souris <= largeurFenetre // 2 - 40 :
                            rectangle(largeurFenetre // 2 - 100, hauteurFenetre // 2 + 80, largeurFenetre // 2 - 40, hauteurFenetre // 2 + 50, "red", epaisseur=2, tag="cadre")
                            if tev == "ClicGauche" :
                                return None
                        elif largeurFenetre // 2 + 40 <= x_souris <= largeurFenetre // 2 + 100 :
                            rectangle(largeurFenetre // 2 + 100, hauteurFenetre // 2 + 80, largeurFenetre // 2 + 40, hauteurFenetre // 2 + 50, "lime", epaisseur=2, tag="cadre")
                            if tev == "ClicGauche" :
                                efface("confirmer")
                                efface("cadre")
                                efface('oui')
                                break
                    if tev == "Quitte" :
                        return None
                    elif tev == "Touche" :
                        if touche(ev) == "Escape" :
                            return None
                    mise_a_jour()


def menu_variantes(largeurFenetre: int, hauteurFenetre: int, path: str, lst_variantes: list) -> tuple :

    rectangle(0,0, largeurFenetre, hauteurFenetre, "black", "black", 1, "bg")
    image(largeurFenetre//2, 125, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))

    carre(100, 250, 100, "white", nom="Cadre")
    texte(150, 300, "Score", "white", "center", taille=14, tag="score")

    carre(235, 250, 100, "white", nom="Cadre")
    texte(285, 300, "Vitesse", "white", "center", taille=14, tag="vitesse")

    carre(370, 250, 100, "white", nom="Cadre")
    texte(420, 300, "  Deux\nJoueurs", "white", "center", taille=14, tag="2joueurs")

    carre(100, 400, 100, "white", nom="Cadre")
    texte(150, 450, "Obstacles", "white", "center", taille=14, tag="obstacles")

    carre(235, 400, 100, "white", nom="Cadre")
    texte(285, 450, "Bonus", "white", "center", taille=14, tag="bonus")

    carre(100, 550, 100, "white", nom="Cadre")
    texte(150, 600, " Sparx\nInternes", "white", "center", taille=14, tag="sparx")

    carre(235, 550, 100, "white", nom="Cadre")
    texte(285, 600, "Niveaux", "white", "center", taille=14, tag="niveaux")

    rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 150, largeurFenetre // 2 + 200, hauteurFenetre - 200, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, hauteurFenetre - 175, "Menu Principal", "white", "center", taille=24, tag="Principal")

    for variante in lst_variantes :
        if variante == "Score" :
            carre(100, 250, 100, "lime", nom="highlight_score")
        elif variante == "Obstacles" :
            carre(100, 400, 100, "lime", nom="highlight_obstacles")
        elif variante == "Sparx" :
            carre(100, 550, 100, "lime", nom="highlight_sparx")
        elif variante == "Vitesse" :
            carre(235, 250, 100, "lime", nom="highlight_vitesse")
        elif variante == "Bonus" :
            carre(235, 400, 100, "lime", nom="highlight_bonus")
        elif variante == "Niveaux" :
            carre(235, 550, 100, "lime", nom="highlight_niveaux")
        elif variante == "Joueurs" :
            carre(370, 250, 100, "lime", nom="highlight_joueurs")

    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        if largeurFenetre // 2 - 200 <= x_souris <= largeurFenetre // 2 + 200 :
            if hauteurFenetre - 200 <= y_souris <= hauteurFenetre - 150 :
                rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 150, largeurFenetre // 2 + 200, hauteurFenetre - 200, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Principal", lst_variantes
        if 100 <= x_souris <= 200 :
            if 250 <= y_souris <= 350 :
                carre(100, 250, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Score" in lst_variantes :
                        efface("highlight_score")
                        lst_variantes.remove("Score")
                    else :
                        carre(100, 250, 100, "lime", nom="highlight_score")
                        lst_variantes.append("Score")
            elif 400 <= y_souris <= 500 :
                carre(100, 400, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Obstacles" in lst_variantes :
                        efface("highlight_obstacles")
                        lst_variantes.remove("Obstacles")
                    else :
                        carre(100, 400, 100, "lime", nom="highlight_obstacles")
                        lst_variantes.append("Obstacles")
            elif 550 <= y_souris <= 650 :
                carre(100, 550, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Sparx" in lst_variantes :
                        efface("highlight_sparx")
                        lst_variantes.remove("Sparx")
                    else :
                        carre(100, 550, 100, "lime", nom="highlight_sparx")
                        lst_variantes.append("Sparx")
        elif 235 <= x_souris <= 335 :
            if 250 <= y_souris <= 350 :
                carre(235, 250, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Vitesse" in lst_variantes :
                        efface("highlight_vitesse")
                        lst_variantes.remove("Vitesse")
                    else :
                        carre(235, 250, 100, "lime", nom="highlight_vitesse")
                        lst_variantes.append("Vitesse")
            elif 400 <= y_souris <= 500 :
                carre(235, 400, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Bonus" in lst_variantes :
                        efface("highlight_bonus")
                        lst_variantes.remove("Bonus")
                    else :
                        carre(235, 400, 100, "lime", nom="highlight_bonus")
                        lst_variantes.append("Bonus")
            elif 550 <= y_souris <= 650 :
                carre(235, 550, 100, "blue", nom="rectangle", taille=1.25)
                if tev == "ClicGauche" :
                    if "Niveaux" in lst_variantes :
                        efface("highlight_niveaux")
                        lst_variantes.remove("Niveaux")
                    else :
                        carre(235, 550, 100, "lime", nom="highlight_niveaux")
                        lst_variantes.append("Niveaux")
        elif 370 <= x_souris <= 470 :
            if 250 <= y_souris <= 350 :
                carre(370, 250, 100, "blue", nom="rectangle")
                if tev == "ClicGauche" :
                    if "Joueurs" in lst_variantes :
                        efface("highlight_joueurs")
                        lst_variantes.remove("Joueurs")
                    else :
                        carre(370, 250, 100, "lime", nom="highlight_joueurs")
                        lst_variantes.append("Joueurs")
        mise_a_jour()
        if tev == "Quitte" :
            break
        if touche_pressee("Escape") :
            return "Principal", lst_variantes
    return None, []


def menu_parametres(largeurFenetre: int, hauteurFenetre: int, path: str) -> str :
    rectangle(0,0, largeurFenetre, hauteurFenetre, "black", "black", 1, "bg")
    image(largeurFenetre//2,125, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))

    rectangle(largeurFenetre // 2 - 200, 250, largeurFenetre // 2 + 200, 300, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 275, "Options des ennemis", "white", "center", taille=24, tag="options")

    rectangle(largeurFenetre // 2 - 200, 325, largeurFenetre // 2 + 200, 375, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, 350, "Touches", "white", "center", taille=24, tag="touches")

    rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 150, largeurFenetre // 2 + 200, hauteurFenetre - 200, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, hauteurFenetre - 175, "Menu Principal", "white", "center", taille=24, tag="Principal")

    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        if largeurFenetre // 2 - 200 <= x_souris <= largeurFenetre // 2 + 200 :
            if 250 <= y_souris <= 300 :
                rectangle(largeurFenetre // 2 - 200, 250,largeurFenetre // 2 + 200, 300, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Options"
            elif 325 <= y_souris <= 375 :
                rectangle(largeurFenetre // 2 - 200, 325,largeurFenetre // 2 + 200, 375, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Touches"
            if hauteurFenetre - 200 <= y_souris <= hauteurFenetre - 150 :
                rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 150, largeurFenetre // 2 + 200, hauteurFenetre - 200, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Principal"
        
        mise_a_jour()
        if tev == "Quitte" :
            break
        elif tev == "Touche" :
            if touche(ev) == "Escape" :
                return "Principal"

def menu_options(largeurFenetre: int, hauteurFenetre: int, path: str, lst_options: list) -> tuple :
    rectangle(0,0, largeurFenetre, hauteurFenetre, "black", "black", 1, "bg")
    image(largeurFenetre//2,125, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))

    entree = ""

    rectangle(65, 200, 335, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(200, 245, "Divers", "#45FFCA", "center", tag="titre")
    ligne(65, 290, 335, 290, "#45FFCA", 3, "ligne")


    rectangle(75, 300, 275, 350, "white", epaisseur=2, tag="cadre")
    texte(175, 325, "Nombre d'obstacles", "white", "center", taille=15, tag="obstacles")
    rectangle(275, 299, 325, 350, "white", tag="bouton")
    texte(300, 325, lst_options[0], "white", "center", taille=15, tag="nombre_obstacles")

    rectangle(75, 375, 275, 425, "white", epaisseur=2, tag="cadre")
    texte(175, 400, "Nombre de bonus", "white", "center", taille=15, tag="bonus")
    rectangle(275, 374, 325, 425, "white", tag="bouton")
    texte(300, 400, lst_options[1], "white", "center", taille=15, tag="nombre_pommes")

    rectangle(75, 450, 275, 500, "white", epaisseur=2, tag="cadre")
    texte(175, 475, "Nombre de vies", "white", "center", taille=15, tag="vies")
    rectangle(275, 449, 325, 500, "white", tag="bouton")
    texte(300, 475, lst_options[2], "white", "center", taille=15, tag="nombre_vies")

    rectangle(75, 525, 275, 575, "white", epaisseur=2, tag="cadre")
    texte(175, 550, "Niveau initial", "white", "center", taille=15, tag="niveau")
    rectangle(275, 524, 325, 575, "white", tag="bouton")
    texte(300, 550, lst_options[3], "white", "center", taille=13, tag="nb_niveau")

    rectangle(75, 600, 275, 650, "white", epaisseur=2, tag="cadre")
    texte(175, 625, "Vitesse joueur (normal)", "white", "center", taille=14, tag="JoueurSpd(n)")
    rectangle(275, 599, 325, 650, "white", tag="bouton")
    texte(300, 625, lst_options[4], "white", "center", taille=15, tag="nombre_JoueurSpd(n)")

    rectangle(75, 675, 275, 725, "white", epaisseur=2, tag="cadre")
    texte(175, 700, "Vitesse joueur (rapide)", "white", "center", taille=14, tag="JoueurSpd(f)")
    rectangle(275, 674, 325, 725, "white", tag="bouton")
    texte(300, 700, lst_options[5], "white", "center", taille=15, tag="nombre_JoueurSpd(f)")




    rectangle(365, 200, 635, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(500, 245, "Initialisation", "#45FFCA", "center", tag="titre")
    ligne(365, 290, 635, 290, "#45FFCA", 3, "ligne")


    rectangle(375, 300, 575, 350, "white", epaisseur=2, tag="cadre")
    texte(475, 325, "Vitesse du QIX", "white", "center", taille=15, tag="QIXspdI")
    rectangle(575, 299, 625, 350, "white", tag="bouton")
    texte(600, 325, lst_options[6], "white", "center", taille=15, tag="nb_QIXspdI")

    rectangle(375, 375, 575, 425, "white", epaisseur=2, tag="cadre")
    texte(475, 400, "Vitesse du Sparx", "white", "center", taille=15, tag="SparxspdI")
    rectangle(575, 374, 625, 425, "white", tag="bouton")
    texte(600, 400, lst_options[7], "white", "center", taille=15, tag="nb_SparxspdI")

    rectangle(375, 450, 575, 500, "white", epaisseur=2, tag="cadre")
    texte(475, 475, "Zone à capturer", "white", "center", taille=15, tag="zone_a_capturerI")
    rectangle(575, 449, 625, 500, "white", tag="bouton")
    texte(600, 475, lst_options[8] + " %", "white", "center", taille=14, tag="nb_zone_a_capturerI")

    rectangle(375, 525, 575, 575, "white", epaisseur=2, tag="cadre")
    texte(475, 550, "Taille du QIX", "white", "center", taille=14, tag="tailleQIX")
    rectangle(575, 524, 625, 575, "white", tag="bouton")
    texte(600, 550, lst_options[9], "white", "center", taille=15, tag="nb_tailleQIX")

    rectangle(375, 600, 575, 650, "white", epaisseur=2, tag="cadre")
    texte(475, 625, "Taille du Joueur", "white", "center", taille=15, tag="tailleJoueur")
    rectangle(575, 599, 625, 650, "white", tag="bouton")
    texte(600, 625, lst_options[10], "white", "center", taille=15, tag="nb_tailleJoueur")



    rectangle(665, 200, 935, 435, "#45FFCA", epaisseur=3, tag="cadre")
    texte(800, 230, "Incrémentation", "#45FFCA", "center", tag="titre")
    texte(800, 260, "par niveau", "#45FFCA", "center", tag="titre")
    ligne(665, 290, 935, 290, "#45FFCA", 3, "ligne")


    rectangle(675, 300, 875, 350, "white", epaisseur=2, tag="cadre")
    texte(775, 325, "Vitesse du QIX", "white", "center", taille=15, tag="QIXspd+")
    rectangle(875, 299, 925, 350, "white", tag="bouton")
    texte(900, 325, lst_options[11], "white", "center", taille=15, tag="nb_QIXspd+")

    rectangle(675, 375, 875, 425, "white", epaisseur=2, tag="cadre")
    texte(775, 400, "Vitesse du Sparx", "white", "center", taille=15, tag="Sparxspd+")
    rectangle(875, 374, 925, 425, "white", tag="bouton")
    texte(900, 400, lst_options[12], "white", "center", taille=15, tag="nb_Sparxspd+")


    rectangle(665, 445, 935, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(800, 475, "Incrémentation", "#45FFCA", "center", tag="titre")
    texte(800, 505, "par "+ lst_options[13] +" niveaux", "#45FFCA", "center", tag="titre")
    ligne(665, 535, 935, 535, "#45FFCA", 3, "ligne")

    rectangle(675, 545, 875, 595, "white", epaisseur=2, tag="cadre")
    texte(775, 570, "Incrémentation par", "white", "center", taille=15, tag="+")
    rectangle(875, 544, 925, 595, "white", tag="bouton")
    texte(900, 570, lst_options[13], "white", "center", taille=15, tag="nb_+")

    rectangle(675, 620, 875, 670, "white", epaisseur=2, tag="cadre")
    texte(775, 645, "Zone à capturer", "white", "center", taille=15, tag="zone_a_capturer+")
    rectangle(875, 619, 925, 670, "white", tag="bouton")
    texte(900, 645, lst_options[14] + " %", "white", "center", taille=15, tag="nb_zone_a_capturer+")


    rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 100, largeurFenetre // 2 + 200, hauteurFenetre - 150, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, hauteurFenetre - 125, "Paramètres", "white", "center", taille=24, tag="Parametres")

    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        if largeurFenetre // 2 - 200 <= x_souris <= largeurFenetre // 2 + 200 :
            if hauteurFenetre - 150 <= y_souris <= hauteurFenetre - 100 :
                rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 100, largeurFenetre // 2 + 200, hauteurFenetre - 150, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Parametres", lst_options
        if 275 <= x_souris <= 325 :
            if 299 <= y_souris <= 350 :
                rectangle(275, 299, 325, 350, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nombre_obstacles")
                    entree = input(True)
                    if entree != "" :
                        lst_options[0] = entree
                    texte(300, 325, lst_options[0], "white", "center", taille=15, tag="nombre_obstacles")
            elif 374 <= y_souris <= 425 :
                rectangle(275, 374, 325, 425, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nombre_pommes")
                    entree = input(True)
                    if entree != "" :
                        lst_options[1] = entree
                    texte(300, 400, lst_options[1], "white", "center", taille=15, tag="nombre_pommes")
            elif 449 <= y_souris <= 500 :
                rectangle(275, 449, 325, 500, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nombre_vies")
                    entree = input(True)
                    if entree != "" and entree > "0" and ("." not in entree) :
                        lst_options[2] = entree
                    texte(300, 475, lst_options[2], "white", "center", taille=15, tag="nombre_vies")
            elif 524 <= y_souris <= 575 :
                rectangle(275, 524, 325, 575, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_niveau")
                    entree = input(True)
                    if entree != "" and entree > "0" and ("." not in entree) :
                        lst_options[3] = entree
                    texte(300, 550, lst_options[3], "white", "center", taille=15, tag="nb_niveau")
            elif 599 <= y_souris <= 650 :
                rectangle(275, 599, 325, 650, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nombre_JoueurSpd(n)")
                    entree = input(True)
                    if entree != "" :
                        lst_options[4] = entree
                    texte(300, 625, lst_options[4], "white", "center", taille=15, tag="nombre_JoueurSpd(n)")
            elif 674 <= y_souris <= 725 :
                rectangle(275, 674, 325, 725, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nombre_JoueurSpd(f)")
                    entree = input(True)
                    if entree != "" :
                        lst_options[5] = entree
                    texte(300, 700, lst_options[5], "white", "center", taille=15, tag="nombre_JoueurSpd(f)")
        elif 575 <= x_souris <= 625 :
            if 299 <= y_souris <= 350 :
                rectangle(575, 299, 625, 350, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_QIXspdI")
                    entree = input(True)
                    if entree != "" :
                        lst_options[6] = entree
                    texte(600, 325, lst_options[6], "white", "center", taille=15, tag="nb_QIXspdI")
            elif 374 <= y_souris <= 425 :
                rectangle(575, 374, 625, 425, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_SparxspdI")
                    entree = input(True)
                    if entree != "" :
                        lst_options[7] = entree
                    texte(600, 400, lst_options[7], "white", "center", taille=15, tag="nb_SparxspdI")
            elif 449 <= y_souris <= 500 :
                rectangle(575, 449, 625, 500, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_zone_a_capturerI")
                    entree = input(True)
                    if entree != "" and entree > "0" and entree < "100" :
                        lst_options[8] = entree
                    texte(600, 475, lst_options[8] + " %", "white", "center", taille=13, tag="nb_zone_a_capturerI")
            elif 524 <= y_souris <= 575 :
                rectangle(575, 524, 625, 575, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_tailleQIX")
                    entree = input(True)
                    if entree != "" :
                        lst_options[9] = entree
                    texte(600, 550, lst_options[9], "white", "center", taille=15, tag="nb_tailleQIX")
            elif 599 <= y_souris <= 650 :
                rectangle(575, 599, 625, 650, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_tailleJoueur")
                    entree = input(True)
                    if entree != "" :
                        lst_options[10] = entree
                    texte(600, 625, lst_options[10], "white", "center", taille=15, tag="nb_tailleJoueur")
        elif 875 <= x_souris <= 925 :
            if 299 <= y_souris <= 350 :
                rectangle(875, 299, 925, 350, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_QIXspd+")
                    entree = input(True)
                    if entree != "" :
                        lst_options[11] = entree
                    texte(900, 325, lst_options[11], "white", "center", taille=15, tag="nb_QIXspd+")
            elif 374 <= y_souris <= 425 :
                rectangle(875, 374, 925, 425, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_Sparxspd+")
                    entree = input(True)
                    if entree != "" :
                        lst_options[12] = entree
                    texte(900, 400, lst_options[12], "white", "center", taille=15, tag="nb_Sparxspd+")
            elif 544 <= y_souris <= 595 :
                rectangle(875, 544, 925, 595, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_+")
                    entree = input(True)
                    if entree != "" and entree > "0" :
                        lst_options[13] = entree
                    texte(900, 570, lst_options[13], "white", "center", taille=15, tag="nb_+")
            elif 619 <= y_souris <= 670 :
                rectangle(875, 619, 925, 670, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("nb_zone_a_capturer+")
                    entree = input(True)
                    if entree != "" :
                        lst_options[14] = entree
                    texte(900, 645, lst_options[14] + " %", "white", "center", taille=15, tag="nb_zone_a_capturer+")
        mise_a_jour()
        if tev == "Quitte" :
            break
        elif tev == "Touche" :
            if touche(ev) == "Escape" :
                return "Parametres", lst_options
    return None, lst_options

def input(nombre: bool) -> str :
    """nombre est un bouléen qui permet d'activer uniquement les chiffres dans le mot renvoyé"""
    texte = ""
    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Touche" :
            nom_touche = touche(ev)
            if nom_touche == "Escape" :
                return ""
            elif not nombre :
                return nom_touche
            else :
                if nom_touche in string.digits :
                    texte = texte + nom_touche
                elif nom_touche == "period" :
                    texte = texte + "."
                elif nom_touche == "Return" : 
                    if texte[-1] == "." :
                        texte = texte[:-1]
                    break
        elif tev == "Quitte" :
            ferme_fenetre()
        mise_a_jour()
    return texte

def menu_touches(largeurFenetre: int, hauteurFenetre: int, path: str, lst_touches: list) -> tuple :
    rectangle(0,0, largeurFenetre, hauteurFenetre, "black", "black", 1, "bg")
    image(largeurFenetre//2,125, os.path.join(path,'QIX_logo.gif'), ancrage="center", tag="im", largeur=300, hauteur=int(188*(300/414)))

    entree = ""

    rectangle(65, 200, 335, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(200, 245, "Joueur 1", "#45FFCA", "center", tag="titre")
    ligne(65, 290, 335, 290, "#45FFCA", 3, "ligne")


    rectangle(75, 300, 275, 350, "white", epaisseur=2, tag="cadre")
    texte(175, 325, "Monter", "white", "center", taille=15, tag="monter")
    rectangle(275, 299, 325, 350, "white", tag="bouton")
    texte(300, 325, lst_touches[0], "white", "center", taille=15, tag="touche_monter1")

    rectangle(75, 375, 275, 425, "white", epaisseur=2, tag="cadre")
    texte(175, 400, "A gauche", "white", "center", taille=15, tag="gauche")
    rectangle(275, 374, 325, 425, "white", tag="bouton")
    texte(300, 400, lst_touches[1], "white", "center", taille=15, tag="touche_gauche1")

    rectangle(75, 450, 275, 500, "white", epaisseur=2, tag="cadre")
    texte(175, 475, "Descendre", "white", "center", taille=15, tag="descendre")
    rectangle(275, 449, 325, 500, "white", tag="bouton")
    texte(300, 475, lst_touches[2], "white", "center", taille=15, tag="touche_descendre1")

    rectangle(75, 525, 275, 575, "white", epaisseur=2, tag="cadre")
    texte(175, 550, "A droite", "white", "center", taille=15, tag="droite")
    rectangle(275, 524, 325, 575, "white", tag="bouton")
    texte(300, 550, lst_touches[3], "white", "center", taille=13, tag="touche_droite1")

    rectangle(75, 600, 275, 650, "white", epaisseur=2, tag="cadre")
    texte(175, 625, "Vitesse normale", "white", "center", taille=14, tag="spd(n)1")
    rectangle(275, 599, 325, 650, "white", tag="bouton")
    texte(300, 625, lst_touches[4], "white", "center", taille=15, tag="touche_spd(n)1")

    rectangle(75, 675, 275, 725, "white", epaisseur=2, tag="cadre")
    texte(175, 700, "Vitesse rapide", "white", "center", taille=14, tag="spd(f)1")
    rectangle(275, 674, 325, 725, "white", tag="bouton")
    texte(300, 700, lst_touches[5], "white", "center", taille=15, tag="touche_spd(f)1")




    rectangle(365, 200, 635, 735, "#45FFCA", epaisseur=3, tag="cadre")
    texte(500, 245, "Joueur 2", "#45FFCA", "center", tag="titre")
    ligne(365, 290, 635, 290, "#45FFCA", 3, "ligne")


    rectangle(375, 300, 575, 350, "white", epaisseur=2, tag="cadre")
    texte(475, 325, "Monter", "white", "center", taille=15, tag="monter2")
    rectangle(575, 299, 625, 350, "white", tag="bouton")
    texte(600, 325, lst_touches[6], "white", "center", taille=15, tag="touche_monter2")

    rectangle(375, 375, 575, 425, "white", epaisseur=2, tag="cadre")
    texte(475, 400, "A gauche", "white", "center", taille=15, tag="gauche2")
    rectangle(575, 374, 625, 425, "white", tag="bouton")
    texte(600, 400, lst_touches[7], "white", "center", taille=15, tag="touche_gauche2")

    rectangle(375, 450, 575, 500, "white", epaisseur=2, tag="cadre")
    texte(475, 475, "Descendre", "white", "center", taille=15, tag="descendre2")
    rectangle(575, 449, 625, 500, "white", tag="bouton")
    texte(600, 475, lst_touches[8], "white", "center", taille=14, tag="touche_descendre2")

    rectangle(375, 525, 575, 575, "white", epaisseur=2, tag="cadre")
    texte(475, 550, "A droite", "white", "center", taille=14, tag="droite2")
    rectangle(575, 524, 625, 575, "white", tag="bouton")
    texte(600, 550, lst_touches[9], "white", "center", taille=15, tag="touche_droite2")

    rectangle(375, 600, 575, 650, "white", epaisseur=2, tag="cadre")
    texte(475, 625, "Vitesse normale", "white", "center", taille=15, tag="spd(n)2")
    rectangle(575, 599, 625, 650, "white", tag="bouton")
    texte(600, 625, lst_touches[10], "white", "center", taille=15, tag="touche_spd(n)2")

    rectangle(375, 675, 575, 725, "white", epaisseur=2, tag="cadre")
    texte(475, 700, "Vitesse rapide", "white", "center", taille=14, tag="spd(f)2")
    rectangle(575, 674, 625, 725, "white", tag="bouton")
    texte(600, 700, lst_touches[11], "white", "center", taille=15, tag="touche_spd(f)2")


    rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 100, largeurFenetre // 2 + 200, hauteurFenetre - 150, "white", epaisseur=2, tag="bouton")
    texte(largeurFenetre // 2, hauteurFenetre - 125, "Paramètres", "white", "center", taille=24, tag="Parametres")
    
    while True :
        ev = donne_ev()
        tev = type_ev(ev)
        x_souris = abscisse_souris()
        y_souris = ordonnee_souris()
        efface("rectangle")
        if largeurFenetre // 2 - 200 <= x_souris <= largeurFenetre // 2 + 200 :
            if hauteurFenetre - 150 <= y_souris <= hauteurFenetre - 100 :
                rectangle(largeurFenetre // 2 - 200, hauteurFenetre - 100, largeurFenetre // 2 + 200, hauteurFenetre - 150, "blue", epaisseur=2, tag="rectangle")
                if tev == "ClicGauche" :
                    return "Parametres", lst_touches
        if 275 <= x_souris <= 325 :
            if 299 <= y_souris <= 350 :
                rectangle(275, 299, 325, 350, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_monter1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[0] = entree
                    texte(300, 325, lst_touches[0], "white", "center", taille=15, tag="touche_monter1")
            elif 374 <= y_souris <= 425 :
                rectangle(275, 374, 325, 425, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_gauche1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[1] = entree
                    texte(300, 400, lst_touches[1], "white", "center", taille=15, tag="touche_gauche1")
            elif 449 <= y_souris <= 500 :
                rectangle(275, 449, 325, 500, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_descendre1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[2] = entree
                    texte(300, 475, lst_touches[2], "white", "center", taille=15, tag="touche_descendre1")
            elif 524 <= y_souris <= 575 :
                rectangle(275, 524, 325, 575, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_droite1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[3] = entree
                    texte(300, 550, lst_touches[3], "white", "center", taille=15, tag="touche_droite1")
            elif 599 <= y_souris <= 650 :
                rectangle(275, 599, 325, 650, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_spd(n)1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[4] = entree
                    texte(300, 625, lst_touches[4], "white", "center", taille=15, tag="touche_spd(n)1")
            elif 674 <= y_souris <= 725 :
                rectangle(275, 674, 325, 725, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_spd(f)1")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[5] = entree
                    texte(300, 700, lst_touches[5], "white", "center", taille=15, tag="touche_spd(f)1")
        elif 575 <= x_souris <= 625 :
            if 299 <= y_souris <= 350 :
                rectangle(575, 299, 625, 350, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_monter2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[6] = entree
                    texte(600, 325, lst_touches[6], "white", "center", taille=15, tag="touche_monter2")
            elif 374 <= y_souris <= 425 :
                rectangle(575, 374, 625, 425, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_gauche2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[7] = entree
                    texte(600, 400, lst_touches[7], "white", "center", taille=15, tag="touche_gauche2")
            elif 449 <= y_souris <= 500 :
                rectangle(575, 449, 625, 500, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_descendre2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[8] = entree
                    texte(600, 475, lst_touches[8], "white", "center", taille=13, tag="touche_descendre2")
            elif 524 <= y_souris <= 575 :
                rectangle(575, 524, 625, 575, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_droite2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[9] = entree
                    texte(600, 550, lst_touches[9], "white", "center", taille=13, tag="touche_droite2")
            elif 599 <= y_souris <= 650 :
                rectangle(575, 599, 625, 650, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_spd(n)2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[10] = entree
                    texte(600, 625, lst_touches[10], "white", "center", taille=15, tag="touche_spd(n)2")
            elif 674 <= y_souris <= 725 :
                rectangle(575, 674, 625, 725, "blue", tag="rectangle")
                if tev == "ClicGauche" :
                    efface("touche_spd(f)2")
                    entree = input(False)
                    if entree != "" and entree not in lst_touches :
                        lst_touches[11] = entree
                    texte(600, 625, lst_touches[11], "white", "center", taille=15, tag="touche_spd(f)2")
        
        mise_a_jour()
        if tev == "Quitte" :
            break
        elif tev == "Touche" :
            if touche(ev) == "Escape" :
                return "Parametres", lst_touches
    return None, lst_touches

if __name__ == "__main__" :
    cree_fenetre(largeurFenetre, hauteurFenetre)
    lst_variantes = []
    lst_options = ["5", "3", "3", "1", "5", "10", "1", "0.75", "75", "10", "10", "0.25", "0.125", "5", "1"]
    lst_touches = ["Up", "Left", "Down", "Right", "Ctrl_R", "Return", "z", "q", "s", "d", "a", "Shift_L"]
    variable = menu_principal(largeurFenetre, hauteurFenetre, path)
    while variable != None :
        efface_tout()
        if variable == "Principal" :
            variable = menu_principal(largeurFenetre, hauteurFenetre, path)
        elif variable == "Variantes" :
            variable, lst_variantes = menu_variantes(largeurFenetre, hauteurFenetre, path, lst_variantes)
            print(lst_variantes)
        elif variable == "Parametres" :
            while variable != None and variable != "Principal" :
                efface_tout()
                if variable == "Parametres" :
                    variable = menu_parametres(largeurFenetre, hauteurFenetre, path)
                elif variable == "Options" :
                    variable, lst_options = menu_options(largeurFenetre, hauteurFenetre, path, lst_options)
                elif variable == "Touches" :
                    variable, lst_touches = menu_touches(largeurFenetre, hauteurFenetre, path, lst_touches)
        elif variable == "Commencer" :
            break
