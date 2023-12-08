#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
#   *                                                                   *
#   *                              Imports                              *
#   *                                                                   *
#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *

from fltk import *
from Calculs import *
from Interface import *
from random import randint
from math import sin, pi

#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
#   *                                                                   *
#   *                             Fonctions                             *
#   *                                                                   *
#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *


def test_perte(cd_debut: list, cd_joueur: list, cd_QIX: list, cote: float, lst_joueur: list) -> bool :
    """Renvoie True si le joueur rentre dans sa trainée ou si le QIX rentre dans la trainée du joueur. Dans le cas contraire, renvoie False."""
    if cd_debut == cd_joueur :
        return True
    for element in lst_joueur :
        if encadrement(cd_QIX[0],element[0],cd_QIX[0]+cote,True,True) :
            if encadrement(cd_QIX[1],element[1],cd_QIX[1] + cote,True,True) :
                return True
        if cd_joueur == element :
            return True
    return False


def test_sortie_safezone(lst_safezone: list, cx: int, cy: int, dx: int, dy: int, dep: int) -> list :
    """Renvoie les coordonnées du point où le joueur est sorti de la safezone. Si le joueur ne sort pas de la safezone, renvoie une liste vide."""
    for i in range (1,len(lst_safezone)-1) :

        if cx - dx == lst_safezone[i][0] and cy - dy == lst_safezone[i][1] :
            if  ((encadrement_deux_sens(lst_safezone[i-1][0],cx,lst_safezone[i][0],True,True) and encadrement_deux_sens(lst_safezone[i-1][1],cy,lst_safezone[i][1],True,True))
            or  (encadrement_deux_sens(lst_safezone[i][0],cx,lst_safezone[i+1][0],True,True) and encadrement_deux_sens(lst_safezone[i][1],cy,lst_safezone[i+1][1],True,True))) :
                    return []
            else :
                return [cx - dx, cy - dy]
          
        if cy - dy == lst_safezone[i][1] :
            if encadrement_deux_sens(lst_safezone[i][0],cx-dx,lst_safezone[i+1][0],False,False) :
                if cy == lst_safezone[i][1] + dep or cy == lst_safezone[i][1] - dep :
                    return [cx - dx, cy - dy]
                    
        elif cx - dx == lst_safezone[i][0] :
            if encadrement_deux_sens(lst_safezone[i][1],cy-dy,lst_safezone[i+1][1],False,False) :
                if cx == lst_safezone[i][0] + dep or cx == lst_safezone[i][0] - dep :
                    return [cx - dx, cy - dy]
          
    return []


def test_entree_safezone(lst_safezone: list, cx: int, cy: int) -> bool :
    """Renvoie True si le joueur rentre dans la safezone."""
    for i in range (len(lst_safezone)-1) :
        if (encadrement_deux_sens(lst_safezone[i][0],cx,lst_safezone[i+1][0],True,True)) and cy == lst_safezone[i][1] :
            return True
        
        elif (encadrement_deux_sens(lst_safezone[i][1],cy,lst_safezone[i+1][1],True,True)) and cx == lst_safezone[i][0] :
            return True
    return False


def test_interieur_safezone(lst_coordonnees: list, cx: float, cy: float) -> bool :
    """Test pour savoir si un point est à l'intérieur d'une liste de coordonnées (lst_coordonnees doit être une matrice avec des listes à l'intérieur de taille différentes)"""
    nb = 0
    for i in range (len(lst_coordonnees)) :
        for j in range (len(lst_coordonnees[i])) :
            if lst_coordonnees[i][j][0] > cx :
                continue
            if j == len(lst_coordonnees[i])-1 :
                if encadrement_deux_sens(lst_coordonnees[i][j][1],cy,lst_coordonnees[i][0][1],True,False) :
                    nb += 1
            else :
                if encadrement_deux_sens(lst_coordonnees[i][j][1],cy,lst_coordonnees[i][j+1][1],True,False) :
                    nb += 1
    if nb % 2 == 0 :
        return False
    else :
        return True
    

def creation_obstacles(nb_obstacles: int) -> list :
    """Crée nb_obstacles obstacles et renvoie la liste avec leurs coordonnées."""
    lst_obstacles = []
    nb_cases_abs = (coin_inf_droite[0] - coin_sup_gauche[0]) // 10
    nb_cases_ord = (coin_inf_droite[1] - coin_sup_gauche[1]) // 10
    for i in range(nb_obstacles) :
        obstacle = [randint(2, nb_cases_abs-2), randint(2, nb_cases_ord-2)]
        while obstacle in lst_obstacles :
            obstacle = [randint(2, nb_cases_abs-2), randint(2, nb_cases_ord-2)]
        obstacle[0] = obstacle[0] * 10 + coin_sup_gauche[0]
        obstacle[1] = obstacle[1] * 10 + coin_sup_gauche[1]
        lst_obstacles.append(obstacle)
        carre(lst_obstacles[i][0], lst_obstacles[i][1], 10, "orange", "orange", "obstacles", 1)
    return lst_obstacles

def mouvement_sparx(cxSparx: float, cySparx: float, cw, last) :   

#           Le code qui suit est très moche (et le Sparx qui tourne dans le sens inverse des aiguilles d'une montre ne fonctionne pas bien,
#           j'ai des problèmes avec ses déplacements, donc j'ai préféré lui retirer le fait de tenter d'aller dans la zone
#           de jeu plutôt que de le laisser et qu'il se retrouve bloqué ou qu'il parte dans tous les sens; il bougera quand même sur le cadre, et je changerai dès
#           que je trouverai le problème. Ce défaut vient de mon côté, donc s'il-vous-plaît, ne pénalisez pas Jérémy pour cela, c'est déjà lui qui a fait une
#           grande partie du travail sur ce projet ...) et n'est pas du tout compact/optimisé, j'en suis conscient. (Romain)

    dxSparx, dySparx = 0, 0
    act = 0     # Savoir si a déjà fait une action
 
   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    haut = coin_sup_gauche[1]       # Coordonnée Y de la limite supérieure de la Zone de Jeu
    bas = coin_inf_droite[1]        # Coordonnée Y de la limite inférieure de la ZdJ
    gauche = coin_sup_gauche[0]     # Coordonnée X de la limite latérale gauche de la ZdJ
    droite = coin_inf_droite[0]     # Coordonnée X de la limite latérale droite de la ZdJ

    inleft = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx)              # Test pour savoir si la position à gauche          du Sparx est dans la zone capturée
    inright = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx)             # Test pour savoir si la position à droite          du Sparx est dans la zone capturée
    inup = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx, cySparx-depSparx)                # Test pour savoir si la position au-dessus         du Sparx est dans la zone capturée
    indown = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx, cySparx+depSparx)              # Test pour savoir si la position en-dessous        du Sparx est dans la zone capturée
    inbg = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx+depSparx)       # Test pour savoir si la position en bas à gauche   du Sparx est dans la zone capturée
    inbd = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx+depSparx)       # Test pour savoir si la position en bas à droite   du Sparx est dans la zone capturée
    inhg = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx-depSparx)       # Test pour savoir si la position en haut à gauche  du Sparx est dans la zone capturée
    inhd = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx-depSparx)       # Test pour savoir si la position haut à droite     du Sparx est dans la zone capturée

    h,b = cySparx >= haut+depSparx, cySparx <= bas-depSparx
    g, d = cxSparx >= gauche+depSparx, cxSparx <= droite-depSparx


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # last : Dernière direction

    if cxSparx > droite :
        dxSparx = droite - cxSparx
        act = 1
 
    elif cxSparx < gauche :
        dxSparx = gauche - cxSparx
        act = 1

    elif cySparx > bas :
        dySparx = bas - cySparx
        act = 1
      
    elif cySparx < haut :
        dySparx = haut - cySparx
        act = 1


    #if cw and act == 0:
        # Test pour sortir de la bordure
    #    if inbg and cxSparx == droite and last == "down" and h and b :  # Si Sparx à droite
    #        dxSparx = -2*depSparx
    #        last = "left"

    #    elif inhg and cySparx == bas and last == "left" and g and d :   # Si Sparx en bas
    #        dySparx = -2*depSparx
    #        last = "up"

    #    elif inhd and cxSparx == gauche and last == "up" and h and b :  # Si Sparx à gauche
    #        dxSparx = 2*depSparx
    #        last = "right"
         
    #    elif inbd and cySparx == haut and last == "right" and g and d : # Si Sparx en haut
    #        dySparx = 2*depSparx
    #        last = "down"
         
        # Test pour se déplacer autour de la safezone (intérieur)
    #    elif h and b and d and g :
    #        if inup :                           # Si point haut dans zone :
    #            if inbd :                   # Si bas-droite
    #                dySparx = depSparx
    #                last = "down"
    #            else :                      # Sinon
    #                dxSparx = depSparx
    #                last = "right"
 
    #        elif inleft :                   # Si gauche :
    #            dySparx = -depSparx
    #            last = "up"
 
    #        elif indown :                   # Si bas :
    #            dxSparx = -depSparx
    #            last = "left"
 
    #        elif inright :                  # Si droite :
    #            dySparx = depSparx
    #            last = "down"

    #        elif inbg and last != "left" :  # Si bas-gauche et dernier mvt différent de gauche :
    #            dxSparx = -depSparx         # (utilisé pour empêcher un arrêt du sparx dans une situation)
    #            last = "left"

    #        elif inbd :                     # Si bas-droite :
    #            dySparx = depSparx
    #            last = "down"

    #        elif inhd :                     # Si haut-droite :
    #            if last == "down" :     # Si dernier mvt vers le bas
    #                dxSparx = depSparx
    #                last = "right"

    #            elif last == "right" :  # Si dernier mvt vers la droite
    #                dySparx = depSparx
    #                last = "down"

    #        elif inhg :                     # Si haut-gauche
    #            if last == "right" :             
    #                dySparx = -depSparx
    #                last = "up"
      
    #    if dySparx != 0 or dxSparx != 0 :
    #        act = 1
 

    #if cw is False and act == 0 :
    #    # Test pour sortir de la bordure
    #    if inbd and cxSparx == gauche and last == "down" and h and b :  # Si Sparx à gauche
    #        dxSparx = 2*depSparx
    #        last = "right"

    #    elif inhd and cySparx == bas and last == "right" and g and d :   # Si Sparx en bas
    #        dySparx = -2*depSparx
    #        last = "up"

    #    elif inhg and cxSparx == droite and last == "up" and h and b :  # Si Sparx à droite
    #        dxSparx = -2*depSparx
    #        last = "left"

    #    elif inbg and cySparx == haut and last == "left" and g and d : # Si Sparx en haut
    #        dySparx = 2*depSparx
    #        last = "down"


        # Test pour se déplacer autour de la safezone (intérieur)
    #    elif h and b and d and g :
    #        if inup :                           # Si point haut dans zone :
    #            if inbd :                   # Si bas-droite :
    #                dySparx = depSparx   
    #                last = "up"
    #            else :                      # Sinon
    #                dxSparx = -depSparx
    #                last = "left"
 
    #        elif inleft :                       # Si gauche :
    #            dySparx = depSparx
    #            last = "down"

    #        elif indown :                       # Si bas :
    #            dxSparx = -depSparx
    #            last = "right"

    #        elif inright :                      # Si droite :
    #            dySparx = -depSparx
    #            last = "up"

    #        elif inbg and last != "right" :     # Si bas-gauche et dernier mvt était vers la droite :
    #            dxSparx = -depSparx             # (utilisé pour empêcher un arrêt du sparx dans une situation)
    #            last = "right"

    #        elif inbd :                         # Si bas-droite :
    #            dySparx = depSparx
    #            last = "up"

    #        elif inhd :                         # Si haut-droite
    #            if last == "left" :         # Si dernier mvt était vers la gauche :
    #                dySparx = -depSparx
    #                last = "up"

    #            elif last == "up" :         # Si dernier mvt vers le haut : 
    #                dxSparx = -depSparx
    #                last = "left"

    #        elif inhg :                         # Si haut-gauche :
    #            if last == "down" :             
    #                dxSparx = -depSparx
    #                last = "left"
      
    #    if dxSparx != 0 or dySparx != 0 :
    #        act = 1

    #    else :
    #        act = 0

    if act == 0 :
      
        if cySparx == haut :
            if cxSparx == droite and cw :
                dySparx = depSparx
                last = "down"
            elif cxSparx == gauche and cw is False :    # Pour (cw is False), je met l'inverse des instructions, comme celles-ci
                dySparx = -depSparx                     # seront inversés par la suite
                last = "up"
            else :
                dxSparx = depSparx
                last = "right"

        elif cxSparx == droite :
            if cySparx == bas and cw :
                dxSparx = -depSparx
                last = "left"
            elif cySparx == haut and cw is False :
                dySparx = depSparx
                last = "haut"
            else :
                dySparx = depSparx
                last = "down"
 
        elif cySparx == bas :
            if cxSparx == gauche and cw :
                dySparx = -depSparx
                last = "up"
            elif cxSparx == droite and cw is False :
                dySparx = depSparx
                last = "down"
            else :
                dxSparx = -depSparx
                last = "left"
 
        elif cxSparx == gauche :
            if cySparx == haut and cw :
                dxSparx = depSparx
                last = "right"
            elif cySparx == bas and cw is False :
                dxSparx = -depSparx
                last = "left"
            else :
                dySparx = -depSparx
                last = "up"

        if (cw is False) :                                             # Si tourne dans sens inverse des aiguilles d'une montre
            if last == "left" :
                last = "right"
            elif last == "right" :
                last = "left"
            elif last == "up" :
                last = "down"
            elif last == "down" :
                last = "up"
            return -dxSparx, -dySparx, last
     
    return dxSparx, dySparx, last



#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
#   *                                                                   *
#   *                           Code Principal                          *
#   *                                                                   *
#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *

#   .   .   .   .   .   Variables à initialiser pour l'export   .   .   .   .   .

zonetot = 0     # Ratio entre les zones capturées par les joueurs et le terrain de jeu
zone_a_capture = 75
nbVies = 3
niveau = 1
score = 0

#   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .


if __name__ == "__main__" :

   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
   #   *               Mise en place des différents éléments               *
   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *



   #   ========= Définition de la zone de jeu =========


    coin_sup_gauche, coin_inf_droite = ecran_launch()                 
    Perdu = False
    dessiner = False
    nb_delai = 10                   
    # Nombre qui indique le délai entre les déplacements du QIX

    a = 0
    # Nombre qui incrémente à chaque exécution d'une boucle


    cx, cy, rayon = largeurFenetre // 2, coin_inf_droite[1], 5   #  -   -   -   -   -   -   -   Taille et position du curseur
    curseur(cx, cy, rayon)


   #   ========= Définition du Qix =========


    cxQIX = largeurFenetre // 2                   
    cyQIX = (coin_inf_droite[1] - coin_sup_gauche[1]) / 4 + coin_sup_gauche[1]
    carre(cxQIX-5,cyQIX-5,10,"Red","Red","QIX",None)


   #   ========= Définition des Sparx =========


    cxSparx1, cxSparx2 = largeurFenetre // 2, largeurFenetre // 2
    cySparx1, cySparx2 = coin_sup_gauche[1], coin_sup_gauche[1] 
    coor_spx1, coor_spx2 = [500,175], [500,175] 
    sparx1 = sparx(cxSparx1, cySparx1)     # -   Sparx 1
    sparx2 = sparx(cxSparx2, cySparx2)     # -   Sparx 2


   #   ========= Liste des coordonnées =========

    lst_coordonnees_curseur = []
    # Liste des coordonnées des cases où le curseur est passé

    lst_coordonnees_safezone = [[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche,[coin_sup_gauche[0],coin_inf_droite[1]],coin_inf_droite,[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche]
    # Liste des sommets que le joueur n'a pas encore capturé

    lst_coordonnees_polygones = [[coin_sup_gauche,[coin_inf_droite[0],coin_sup_gauche[1]],coin_inf_droite,[coin_sup_gauche[0],coin_inf_droite[1]]]]
    # Coordonnées des différents polygones formés par le joueur

    coordonnees_debut = []
    # Coordonnée de la case où le joueur sort de la bordure

    coordonnees_supprime = None
    # Coordonnées qui sont supprimées de la safezone lors de l'exécution de la fonction concatenation_safezone

    coordonnees_debut_safezone = [[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche]
    # Coordonnées au début (ou à la fin) de la safezone uniquement utile pour la fonction debut_egal_fin

    lst_obstacles = creation_obstacles(5)
    # Coordonnées des obstacles


    zonemax = aire([[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche,[coin_sup_gauche[0],coin_inf_droite[1]],coin_inf_droite,[800,175],coin_sup_gauche], True)
    # Aire total de la zone de jeu

    dep = 5
    # Vitesse de déplacement du Joueur

    depQIX = 1
    # Vitesse de déplacement du QIX

    depSparx = 0.75
    # Vitesse de déplacement des Sparx

    obstacle = False



   #   .   .   .   .   .   Variables à initialiser .   .   .   .   .


    back,limite_d = "",""
    b = 0
    last1, last2 = "",""



   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
   #   *                                Qix                                *
   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *


    # Les déplacements seront changés, pas assez aléatoire et le Qix a tendance à ne pas beaucoup bouger d'un endroit

    while True :
        if a % nb_delai == 0 :
            a = 0
            dxQIX = 0
            dyQIX = 0
            change = 5
            b += 1
            card = ["nord","sud","est","ouest"]
            if b%change == 0 :         # Choisis la direction aléatoirement, en faisant que celle-ci ne change qu'une fois sur deux
                b = 0
                limite_d = card[randint(0,3)]

            if change is False :    # Inverse le booléen "change"
                change = True
            else :
                change = False

            for i in range(randint(1, 20)) :
                x = randint(0, 6)

                # voir à modifier le déplacement du qix avec du sin et du pi
                if x == 1 :
                    if limite_d == "nord" :
                        dyQIX = max(-depQIX, coin_sup_gauche[1]-10 - cyQIX)                       # Déplacement -> Nord
                    if limite_d == "sud" :
                        dyQIX = min(depQIX, coin_inf_droite[1]+10 - cyQIX)                        # Déplacement -> Sud
                    if limite_d == "est" :
                        dxQIX = min(depQIX, coin_inf_droite[0]+10 - cxQIX)                        # Déplacement -> Est
                    if limite_d == "ouest" :
                        dxQIX = max(-depQIX, coin_sup_gauche[0]-10 - cxQIX)                       # Déplacement -> Ouest
                elif x == 2 :
                    if limite_d != "nord" or limite_d == "est" :
                        dxQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[0]+10 - cxQIX))       # Déplacement -> Nord-Est
                        dyQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[1]-10 - cyQIX))
                    if limite_d == "sud" or limite_d == "ouest" :
                        dxQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[0]-10 - cxQIX))      # Déplacement -> Sud-Ouest
                        dyQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[1]+10 - cyQIX))
                elif x == 3 :
                    if limite_d == "nord" or limite_d == "ouest" :
                        dxQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[0]-10 - cxQIX))      # Déplacement -> Nord-Ouest
                        dyQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[1]-10 - cyQIX))
                    if limite_d == "sud" or limite_d == "est" :
                        dxQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[0]+10 - cxQIX))       # Déplacement -> Sud-Est
                        dyQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[1]+10 - cyQIX))
                if cxQIX + dxQIX > coin_inf_droite[0] or cxQIX + dxQIX < coin_sup_gauche[0] or cyQIX + dyQIX > coin_inf_droite[1] or cyQIX + dyQIX < coin_sup_gauche[1] :
                    break
                   
                if dxQIX != 0 or dyQIX != 0 :
                    if test_interieur_safezone([lst_coordonnees_safezone],cxQIX,cyQIX):
                        cxQIX += -dxQIX
                        cyQIX += -dyQIX
                        efface("QIX")
                        carre(cxQIX-5,cyQIX-5,10,"Red","Red","QIX",None)

                    else :
                        cxQIX += dxQIX
                        cyQIX += dyQIX
                        efface("QIX")
                        carre(cxQIX-5,cyQIX-5,10,"Red","Red","QIX",None)
                 


   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
   #   *                               Sparx                               *
   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *


        #mouvement_sparx(coorX_du_sparx,coorY_du_sparx,[sens horaire ?], dernier_mouv)


        dxSparx1, dySparx1 = 0, 0
        dxSparx1, dySparx1, last1 = mouvement_sparx(cxSparx1, cySparx1, True, last1)
        cxSparx1 += dxSparx1
        cySparx1 += dySparx1

        dxSparx2, dySparx2, last2 = mouvement_sparx(cxSparx2, cySparx2, False, last2)
        cxSparx2 += dxSparx2
        cySparx2 += dySparx2


        efface("Sparx")
        sparx1 = sparx(cxSparx1, cySparx1)
        sparx2 = sparx(cxSparx2, cySparx2)


   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
   #   *                              Joueur                               *
   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *


        ev = donne_ev()
        tev = type_ev(ev)
        dx = 0
        dy = 0

        if touche_pressee('Left'):
            dx = max(-dep, coin_sup_gauche[0] - cx)
        elif touche_pressee('Right'):
            dx = min(dep, coin_inf_droite[0] - cx)
        elif touche_pressee('Down'):
            dy = min(dep, coin_inf_droite[1] - cy)
        elif touche_pressee('Up'):
            dy = max(-dep, coin_sup_gauche[1] - cy)
        
        if touche_pressee('Return') :
            if coordonnees_debut == [] :    # Toggle pour savoir si le joueur dessine ou pas
                dep = 10
                draw(1)
                dessiner = True
        
        if touche_pressee('Control_R') :
            if coordonnees_debut == [] :
                dep = 5
                draw(2)
                dessiner = True

        if dx != 0 or dy != 0 :
            efface('curseur')
            Perdu = test_perte(coordonnees_debut, [cx+dx, cy+dy], [cxQIX-5, cyQIX-5], 10, lst_coordonnees_curseur)
            cx += dx
            cy += dy

            for e in lst_obstacles :
                if encadrement_deux_sens(e[0], cx, e[0] + 10) and encadrement_deux_sens(e[1], cy, e[1]+10) :
                    cx = cx - dx
                    cy = cy - dy
                    obstacle = True
                    break

            if dessiner and not obstacle :
               
                if coordonnees_debut == [] :  # Test pour savoir si le joueur est sur une bordure
                    coordonnees_debut = test_sortie_safezone(lst_coordonnees_safezone, cx, cy, dx, dy, dep)          # Test pour savoir si le joueur sort d'une bordure
                    if coordonnees_debut != [] :
                        if test_interieur_safezone([lst_coordonnees_safezone],cx,cy) :   # Test pour savoir si le joueur sort vers la zone de jeu
                            ligne(cx - dx, cy - dy, cx, cy, "Gold", tag = "Trainée")
                            lst_coordonnees_curseur.append([cx, cy])
                        else :  # Si le joueur ne va pas vers la zone de jeu, il faut annuler le mouvement
                            cx = cx - dx
                            cy = cy - dy
                            coordonnees_debut = []

                else :
                    lst_coordonnees_curseur.append([cx, cy])
                    ligne(cx - dx, cy - dy, cx, cy, "Gold", tag = "Trainée")
                    if Perdu == True :
                        pass
                    elif test_entree_safezone(lst_coordonnees_safezone,cx,cy) :       # Test pour savoir si le joueur entre dans la safezone
                        lst_coordonnees_curseur.insert(0, coordonnees_debut)        # Insertion de la première coordonnée du polygone formé par le joueur
                        lst_coordonnees_curseur = sommets(lst_coordonnees_curseur)  # Fonction pour réduire le nombre de coordonnées dans lst_coordonnees_curseur
                        lst_coordonnees_curseur = cw_a_ccw(lst_coordonnees_curseur) # Fonction pour faire en sorte que les coordonnées du polygone formé par le joueur soit dans le sens contraine de l'aiguille d'une montre (ccw)
                        lst_coordonnees_safezone, coordonnees_supprime = concatenation_safezone(lst_coordonnees_safezone, lst_coordonnees_curseur)  # Ajout et suppression des coordonnées de la safezone

                        if coordonnees_supprime != None :   # Pour ne pas écraser les polygones précedemment faits par le joueur
                            lst_coordonnees_curseur = lst_coordonnees_curseur + coordonnees_supprime

                        couleur = "green" if dep == 10 else "dark blue"

                        if test_interieur_safezone([lst_coordonnees_safezone],cxQIX, cyQIX) :   # Si le QIX est à l'intérieur du polygone, le reste de la zone est capturé
                            polygone(lst_coordonnees_curseur, "white", couleur, tag = "ZoneC")
                            lst_coordonnees_polygones.append(lst_coordonnees_curseur)
                        else :
                            polygone(lst_coordonnees_safezone, "white", couleur, tag = "ZoneC")
                            lst_coordonnees_polygones.append(lst_coordonnees_safezone)
                            lst_coordonnees_safezone = list(lst_coordonnees_curseur)

                        lst_coordonnees_safezone, coordonnees_debut_safezone = debut_egal_fin(lst_coordonnees_safezone, coordonnees_debut_safezone) # Modification des 2 premiers ou derniers éléments de la safezone pour qu'elles soient les mêmes
                        lst_coordonnees_safezone = sommets(lst_coordonnees_safezone)

                        zonetot = ((zonemax - aire(lst_coordonnees_safezone,True)) / zonemax) * 100   # Calcul de l'aire
                        efface("score")
                        score = score + int((aire(lst_coordonnees_safezone,True)*(15-dep))//10000)
                        efface("Trainée")
                        efface("obstacles")
                        for e in lst_obstacles :
                            carre(e[0], e[1], 10, "orange", "orange", "obstacles", 1)
                        efface("Zonecapturee")
                        lst_coordonnees_curseur = []
                        coordonnees_debut = []
                        coordonnees_supprime = None
                        Perdu = False
                        update_act(zonetot, score)
            curseur(cx, cy, rayon)
            obstacle = False





        if encadrement_deux_sens(cxSparx1-5,cx,cxSparx1+5,True,True) and encadrement_deux_sens(cySparx1-5,cy,cySparx1+5,True,True) :    # Si l'un des deux Sparx entre en contact avec le joueur
            Perdu = True
        if encadrement_deux_sens(cxSparx2-5,cx,cxSparx2+5,True,True) and encadrement_deux_sens(cySparx2-5,cy,cySparx2+5,True,True) :
            Perdu = True


        if tev == "Quitte" :
            break


        mise_a_jour()
 




   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
   #   *                        Défaite / Victoire                         *
   #   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
     
        if zonetot >= zone_a_capture :
            niveau += 1
            affichage_gagne(niveau)

            efface('curseur')
            cx, cy = largeurFenetre // 2, coin_inf_droite[1]
            curseur(cx, cy, rayon)

            efface("obstacles")
            lst_obstacles = creation_obstacles(5)

            if niveau%5 == 0 :
                zone_a_capture += 1

            efface("Sparx")
            depSparx += 0.125
            cxSparx1, cxSparx2 = largeurFenetre // 2, largeurFenetre // 2
            cySparx1, cySparx2 = coin_sup_gauche[1], coin_sup_gauche[1]
            sparx1 = sparx(cxSparx1, cySparx1)
            sparx2 = sparx(cxSparx2, cySparx2)

            efface("QIX")
            depQIX += 0.25
            cxQIX = largeurFenetre // 2
            cyQIX = (coin_inf_droite[1] - coin_sup_gauche[1]) / 4 + coin_sup_gauche[1]
            carre(cxQIX-5,cyQIX-5,10,"Red","Red","QIX",None)

            zonetot = 0
            efface("Zonecapturee")
            efface("nbVies")
            efface("Zone_a_capturee")
            efface("niveau")
            efface("score")
            update_act(zonetot, score)
            update_round(zone_a_capture,nbVies,niveau)

            efface("ZoneC")
           
            dessiner = False
            lst_coordonnees_curseur = []
            coordonnees_debut = []
            coordonnees_debut_safezone = [[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche]
            lst_coordonnees_safezone = [[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche,[coin_sup_gauche[0],coin_inf_droite[1]],coin_inf_droite,[coin_inf_droite[0],coin_sup_gauche[1]],coin_sup_gauche]
            lst_coordonnees_polygones = [[coin_sup_gauche,[coin_inf_droite[0],coin_sup_gauche[1]],coin_inf_droite,[coin_sup_gauche[0],coin_inf_droite[1]]]]


        if Perdu == True :
            nbVies -= 1
            affichage_perdu(nbVies)
 
            efface('curseur')
            if coordonnees_debut != [] :
                cx, cy = coordonnees_debut[0], coordonnees_debut[1]
            curseur(cx, cy, rayon)
 
            efface("Sparx")
            cxSparx1, cxSparx2 = largeurFenetre // 2, largeurFenetre // 2
            cySparx1, cySparx2 = coin_sup_gauche[1], coin_sup_gauche[1]
            sparx1 = sparx(cxSparx1, cySparx1)
            sparx2 = sparx(cxSparx2, cySparx2)

            efface("QIX")
            cxQIX = largeurFenetre // 2
            cyQIX = (coin_inf_droite[1] - coin_sup_gauche[1]) / 4 + coin_sup_gauche[1]
            carre(cxQIX-5,cyQIX-5,10,"Red","Red","QIX",None)


            efface("nbVies")
            update_round(zone_a_capture,nbVies,niveau)
            draw(0)
            dep = 6


            dessiner = False
            lst_coordonnees_curseur = []
            coordonnees_debut = []
            Perdu = False
 
            if nbVies == 0 :
                break
     
        a += 1


    ferme_fenetre()
