from typing import List, Set, Tuple, Optional
from Interface.main_screen import start_game
from fltk import *
from Calculs import *

from Interface.menu_controller import menu_controller
from Interface.const import WIDTH, HEIGHT
from Interface.utils import draw_player, draw_sparx, draw_square, draw_status, show_game_over, show_level_complete, update_action, update_round

import random
from math import sin, pi


def test_perte(cd_debut: Tuple[float, float], cd_joueur: Tuple[float, float], cd_QIX: Tuple[float, float], cote: float, lst_joueur: List[Tuple[float, float]]) -> bool:
    """
    Test if the player loses due to collision with QIX or self-intersection.
    
    Args:
        cd_debut: Starting coordinates of player trail
        cd_joueur: Current player coordinates  
        cd_QIX: QIX center coordinates
        cote: QIX size (width/height)
        lst_joueur: List of player trail coordinates
        
    Returns:
        True if collision detected, False otherwise
    """
    # Check if player returned to starting position
    if cd_debut == cd_joueur:
        return True
    
    # Calculate QIX bounds from center coordinates
    qix_half_size = cote / 2
    qix_left = cd_QIX[0] - qix_half_size
    qix_right = cd_QIX[0] + qix_half_size
    qix_top = cd_QIX[1] - qix_half_size
    qix_bottom = cd_QIX[1] + qix_half_size
    
    # Check QIX collision with trail and self-intersection
    for element in lst_joueur:
        # Check if QIX collides with any trail point
        if (qix_left <= element[0] <= qix_right and 
            qix_top <= element[1] <= qix_bottom):
            return True
        # Check for self-intersection
        if cd_joueur == element:
            return True
            
    return False


def test_sortie_safezone(lst_safezone: List[Tuple[float, float]], cx: float, cy: float, dx: float, dy: float, dep: float) -> Optional[Tuple[float, float]]:
    """
    Test if the player exits the safe zone and return the exit coordinates.
    
    Args:
        lst_safezone: List of safe zone boundary coordinates
        cx: Current player x-coordinate
        cy: Current player y-coordinate
        dx: Player x-direction movement
        dy: Player y-direction movement
        dep: Player movement speed/distance
        
    Returns:
        Coordinates where player exited safe zone, None if player stays in safe zone
    """
    for i in range (1, len(lst_safezone)-1) :

        if cx - dx == lst_safezone[i][0] and cy - dy == lst_safezone[i][1] :
            if  ((encadrement_deux_sens(lst_safezone[i-1][0],cx,lst_safezone[i][0],True,True) and encadrement_deux_sens(lst_safezone[i-1][1],cy,lst_safezone[i][1],True,True))
            or  (encadrement_deux_sens(lst_safezone[i][0],cx,lst_safezone[i+1][0],True,True) and encadrement_deux_sens(lst_safezone[i][1],cy,lst_safezone[i+1][1],True,True))) :
                    return
            else :
                return (cx - dx, cy - dy)
          
        if cy - dy == lst_safezone[i][1] :
            if encadrement_deux_sens(lst_safezone[i][0],cx-dx,lst_safezone[i+1][0],False,False) :
                if cy == lst_safezone[i][1] + dep or cy == lst_safezone[i][1] - dep :
                    return (cx - dx, cy - dy)
                    
        elif cx - dx == lst_safezone[i][0] :
            if encadrement_deux_sens(lst_safezone[i][1],cy-dy,lst_safezone[i+1][1],False,False) :
                if cx == lst_safezone[i][0] + dep or cx == lst_safezone[i][0] - dep :
                    return (cx - dx, cy - dy)


def test_entree_safezone(lst_safezone: List[Tuple[float, float]], cx: int, cy: int) -> bool:
    """
    Test if the player re-enters the safe zone.
    
    Args:
        lst_safezone: List of safe zone boundary coordinates
        cx: Player x-coordinate
        cy: Player y-coordinate
        
    Returns:
        True if player enters the safe zone, False otherwise
    """
    for i in range (len(lst_safezone)-1) :
        if (encadrement_deux_sens(lst_safezone[i][0],cx,lst_safezone[i+1][0],True,True)) and cy == lst_safezone[i][1] :
            return True
        
        elif (encadrement_deux_sens(lst_safezone[i][1],cy,lst_safezone[i+1][1],True,True)) and cx == lst_safezone[i][0] :
            return True
    return False


def test_interieur_safezone(lst_coordonnees: List[List[Tuple[float, float]]], cx: float, cy: float) -> bool:
    """
    Test if a point is inside a polygon defined by coordinate lists.
    
    Uses ray casting algorithm to determine if point (cx, cy) is inside
    the polygon(s) defined by lst_coordonnees.
    
    Args:
        lst_coordonnees: Matrix of coordinate lists defining polygon boundaries
        cx: Point x-coordinate to test
        cy: Point y-coordinate to test
        
    Returns:
        True if point is inside any polygon, False otherwise
    """
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
    

def creation_obstacles(nb_obstacles: int, coin_sup_gauche: Tuple[float, float], coin_inf_droite: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Create obstacles and return their coordinate list.
    
    Generates the specified number of obstacles randomly positioned within
    the game area boundaries, avoiding duplicates.
    
    Args:
        nb_obstacles: Number of obstacles to create
        coin_sup_gauche: Top-left corner coordinates of game area
        coin_inf_droite: Bottom-right corner coordinates of game area
        
    Returns:
        List of obstacle coordinates (x, y tuples)
    """
    lst_obstacles = []
    nb_cases_abs = (coin_inf_droite[0] - coin_sup_gauche[0]) // 10
    nb_cases_ord = (coin_inf_droite[1] - coin_sup_gauche[1]) // 10
    for i in range(nb_obstacles) :
        x = random.random() * (nb_cases_abs - 2) + 2
        y = random.random() * (nb_cases_ord - 2) + 2
        obstacle = [x, y]

        # Vérification pour éviter les doublons
        while obstacle in lst_obstacles :
            obstacle = [random.random() * (nb_cases_abs - 2) + 2, random.random() * (nb_cases_ord - 2) + 2]

        # Conversion des coordonnées en pixels
        obstacle[0] = obstacle[0] * 10 + coin_sup_gauche[0]
        obstacle[1] = obstacle[1] * 10 + coin_sup_gauche[1]
        lst_obstacles.append(obstacle)
        draw_square(lst_obstacles[i][0], lst_obstacles[i][1], 10, "orange", "orange", "obstacles")
    return lst_obstacles


def creation_pommes(nb_pommes: int, coin_sup_gauche: Tuple[float, float], coin_inf_droite: Tuple[float, float]) -> List[Tuple[float, float]]:
    """
    Create bonus apples and return their coordinate list.
    
    Generates the specified number of bonus apples randomly positioned within
    the game area boundaries, avoiding duplicates.
    
    Args:
        nb_pommes: Number of bonus apples to create
        coin_sup_gauche: Top-left corner coordinates of game area
        coin_inf_droite: Bottom-right corner coordinates of game area
        
    Returns:
        List of apple coordinates (x, y tuples)
    """
    lst_pommes = []
    nb_cases_abs = (coin_inf_droite[0] - coin_sup_gauche[0]) // 10
    nb_cases_ord = (coin_inf_droite[1] - coin_sup_gauche[1]) // 10
    for i in range(nb_pommes) :
        x = random.random() * (nb_cases_abs - 2) + 2
        y = random.random() * (nb_cases_ord - 2) + 2
        pomme = [x, y]

        # Vérification pour éviter les doublons
        while pomme in lst_pommes :
            pomme = [random.random() * (nb_cases_abs - 2) + 2, random.random() * (nb_cases_ord - 2) + 2]

        # Conversion des coordonnées en pixels
        pomme[0] = pomme[0] * 10 + coin_sup_gauche[0]
        pomme[1] = pomme[1] * 10 + coin_sup_gauche[1]
        lst_pommes.append(pomme)
        cercle(lst_pommes[i][0], lst_pommes[i][1], 5, "red", "red", tag="pommes", epaisseur=1)
    return lst_pommes


def mouvement_sparx(
    cxSparx: float,
    cySparx: float,
    cw: bool, 
    last: str,
    coin_sup_gauche: Tuple[float, float],
    coin_inf_droite: Tuple[float, float],
    depSparx: float
) -> Tuple[float, float, str]:   
    """
    Calculate Sparx enemy movement along the game area boundaries.
    
    Handles Sparx AI movement logic, making them follow the perimeter
    of the safe zone in clockwise or counter-clockwise direction.
    
    Args:
        cxSparx: Current Sparx x-coordinate
        cySparx: Current Sparx y-coordinate  
        cw: Movement direction (True for clockwise, False for counter-clockwise)
        last: Last movement direction taken ("haut", "bas", "gauche", "droite")
        coin_sup_gauche: Top-left corner of game area
        coin_inf_droite: Bottom-right corner of game area
        depSparx: Sparx movement speed/distance
        
    Returns:
        Tuple of (dx, dy, new_direction) for Sparx movement
    """

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

    # inleft = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx)              # Test pour savoir si la position à gauche          du Sparx est dans la zone capturée
    # inright = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx)             # Test pour savoir si la position à droite          du Sparx est dans la zone capturée
    # inup = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx, cySparx-depSparx)                # Test pour savoir si la position au-dessus         du Sparx est dans la zone capturée
    # indown = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx, cySparx+depSparx)              # Test pour savoir si la position en-dessous        du Sparx est dans la zone capturée
    # inbg = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx+depSparx)       # Test pour savoir si la position en bas à gauche   du Sparx est dans la zone capturée
    # inbd = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx+depSparx)       # Test pour savoir si la position en bas à droite   du Sparx est dans la zone capturée
    # inhg = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx-depSparx, cySparx-depSparx)       # Test pour savoir si la position en haut à gauche  du Sparx est dans la zone capturée
    # inhd = not test_interieur_safezone(lst_coordonnees_polygones, cxSparx+depSparx, cySparx-depSparx)       # Test pour savoir si la position haut à droite     du Sparx est dans la zone capturée

    # h,b = cySparx >= haut+depSparx, cySparx <= bas-depSparx
    # g, d = cxSparx >= gauche+depSparx, cxSparx <= droite-depSparx


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
                last = "down"
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



def main() -> None:
    """
    Main game function that runs the QIX game.
    """

    # Initialisation de la fenêtre et des variables de configuration
    cree_fenetre(WIDTH, HEIGHT)
    lst_variantes: Set[str] = set()
    
    options = {
        'obstacles': 5,
        'pommes': 3,
        'vies': 3,
        'nivInit': 1,
        'vitLent': 5,
        'vitRap': 10,
        'vitQIX': 1,
        'vitSp': 0.75,
        'aCapt': 75,
        'QIXSize': 10,
        'PlayerSize': 10,
        'vitQIX+': 0.25,
        'vitSp+': 0.125,
        'niv+': 5,
        'aCapt+': 1
    }
    
    keys = {
        'monter1': 'Up',
        'gauche1': 'Left',
        'bas1': 'Down',
        'droite1': 'Right',
        'lent1': 'Control_R',
        'rapide1': 'Return',
        'monter2': 'z',
        'gauche2': 'q',
        'bas2': 's',
        'droite2': 'd',
        'lent2': 'a',
        'rapide2': 'Shift_L'
    }

    start: bool = menu_controller(lst_variantes, options, keys)
    if not start :
        ferme_fenetre()
        return
    
    #   ========= Définition de la zone de jeu =========
  
    zonetot: float = 0     # Ratio entre les zones capturées par les joueurs et le terrain de jeu
    nbVies: int = int(options['vies'])
    niveau: int = int(options['nivInit'])
    zone_a_capture: float = options['aCapt'] + options['aCapt+'] * (niveau // int(options['niv+']))
    score: Optional[int] = 0 if "Score" in lst_variantes else None

    coin_sup_gauche, coin_inf_droite = start_game(zonetot, zone_a_capture, nbVies, niveau, score)
    dessiner = False

    # Délai entre les déplacements du QIX
    nb_delai = 10

    # Incrémente à chaque exécution d'une boucle
    a = 0



    #   ========= Définition du Joueur =========
    cx: float = WIDTH / 2
    cy: float = coin_inf_droite[1]
    rayon: float = options['PlayerSize'] / 2
    draw_player(cx, cy, rayon)

    #   ========= Définition du Qix =========
    cxQIX: float = WIDTH / 2
    cyQIX: float = (coin_inf_droite[1] - coin_sup_gauche[1]) / 4 + coin_sup_gauche[1]
    draw_square(cxQIX - options['QIXSize'] / 2, cyQIX - options['QIXSize'] / 2, options['QIXSize'], "Red", "Red", "QIX")

    #   ========= Définition des Sparx =========
    cxSparx1: float = float(WIDTH // 2)
    cxSparx2: float = float(WIDTH // 2)
    cySparx1: float = float(coin_sup_gauche[1])
    cySparx2: float = float(coin_sup_gauche[1])
    coor_spx1: Tuple[float, float] = (500, 175)
    coor_spx2: Tuple[float, float] = (500, 175)
    draw_sparx(cxSparx1, cySparx1)     # -   Sparx 1
    draw_sparx(cxSparx2, cySparx2)     # -   Sparx 2

    #   ========= Liste des coordonnées =========

    # Liste des coordonnées des cases où le curseur est passé
    lst_coordonnees_curseur: List[Tuple[float, float]] = []
    
    # Liste des sommets que le joueur n'a pas encore capturé
    lst_coordonnees_safezone: List[Tuple[float, float]] = [
        (coin_inf_droite[0], coin_sup_gauche[1]),
        (coin_sup_gauche[0], coin_sup_gauche[1]),
        (coin_sup_gauche[0], coin_inf_droite[1]),
        (coin_inf_droite[0], coin_inf_droite[1]),
        (coin_inf_droite[0], coin_sup_gauche[1]),
        (coin_sup_gauche[0], coin_sup_gauche[1])
    ]

    # Coordonnées des différents polygones formés par le joueur
    lst_coordonnees_polygones: List[List[Tuple[float, float]]] = [
        [
            (coin_sup_gauche[0], coin_sup_gauche[1]),
            (coin_inf_droite[0], coin_sup_gauche[1]),
            (coin_inf_droite[0], coin_inf_droite[1]),
            (coin_sup_gauche[0], coin_inf_droite[1])
        ]
    ]
    
    # Coordonnée de la case où le joueur sort de la bordure
    coordonnees_debut: Optional[Tuple[float, float]] = None

    # Coordonnées qui sont supprimées de la safezone lors de l'exécution de la fonction concatenation_safezone
    coordonnees_supprime: Optional[List[Tuple[float, float]]] = None
    
    # Coordonnées au début (ou à la fin) de la safezone uniquement utile pour la fonction debut_egal_fin
    coordonnees_debut_safezone: List[Tuple[float, float]] = [
      (coin_inf_droite[0], coin_sup_gauche[1]),
      (coin_sup_gauche[0], coin_sup_gauche[1])
    ]

    # Coordonnées des obstacles et des pommes
    lst_obstacles: Optional[List[Tuple[float, float]]] = None
    lst_pommes: Optional[List[Tuple[float, float]]] = None

    if "Obstacles" in lst_variantes :
        lst_obstacles = creation_obstacles(options['obstacles'], coin_sup_gauche, coin_inf_droite)

    if "Bonus" in lst_variantes :
        lst_pommes = creation_pommes(options['pommes'], coin_sup_gauche, coin_inf_droite)

    # Game constants
    QIX_SIZE_HALF: float = options['QIXSize'] / 2
    
    # Initialize zone calculation total area
    try:
        zonemax: float = aire([
            (coin_inf_droite[0], coin_sup_gauche[1]),
            coin_sup_gauche,
            (coin_sup_gauche[0], coin_inf_droite[1]),
            coin_inf_droite,
            (coin_inf_droite[0], coin_sup_gauche[1]),
            coin_sup_gauche],
            True
        )
    except (ValueError, ZeroDivisionError):
        print("Error calculating initial zone area, using default")
        zonemax = (coin_inf_droite[0] - coin_sup_gauche[0]) * (coin_inf_droite[1] - coin_sup_gauche[1])
    
    # Vitesse de déplacement du Joueur
    
    dep: float = options['vitLent']
    
    # Vitesse de déplacement du QIX
    depQIX: float = options['vitQIX'] + options['vitQIX+'] * (niveau - 1)

    # Vitesse de déplacement des Sparx
    depSparx: float = options['vitSp'] + options['vitSp+'] * (niveau - 1)
    
    perdu: bool = False
    obstacle: bool = False

    # Game state variables
    back: str = ""
    direction_limit: str = ""
    direction_counter: int = 0
    last_sparx1_direction: str = ""
    last_sparx2_direction: str = ""
    
    # Constants
    DIRECTION_CHANGE_INTERVAL: int = 5
    QIX_BOUNDARY_OFFSET: float = 10.0
    COLLISION_TOLERANCE: float = 5.0
    
    while True:
        if a % nb_delai == 0:
            a = 0
            dxQIX = 0
            dyQIX = 0
            direction_counter += 1
            cardinal_directions = ["nord", "sud", "est", "ouest"]
            
            if direction_counter % DIRECTION_CHANGE_INTERVAL == 0:
                direction_counter = 0
                direction_limit = cardinal_directions[random.randint(0, 3)]

            for i in range(random.randint(1, 10)) :
                x = random.randint(0, 6)

                # QIX movement with trigonometric calculations
                if x == 1:
                    if direction_limit == "nord":
                        dyQIX = max(-depQIX, coin_sup_gauche[1] - QIX_BOUNDARY_OFFSET - cyQIX)  # Movement -> North
                    elif direction_limit == "sud":
                        dyQIX = min(depQIX, coin_inf_droite[1] + QIX_BOUNDARY_OFFSET - cyQIX)   # Movement -> South
                    elif direction_limit == "est":
                        dxQIX = min(depQIX, coin_inf_droite[0] + QIX_BOUNDARY_OFFSET - cxQIX)   # Movement -> East
                    elif direction_limit == "ouest":
                        dxQIX = max(-depQIX, coin_sup_gauche[0] - QIX_BOUNDARY_OFFSET - cxQIX)  # Movement -> West
                elif x == 2:
                    if direction_limit in ["nord", "est"]:
                        dxQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[0] + QIX_BOUNDARY_OFFSET - cxQIX))  # Movement -> Northeast
                        dyQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[1] - QIX_BOUNDARY_OFFSET - cyQIX))
                    elif direction_limit in ["sud", "ouest"]:
                        dxQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[0] - QIX_BOUNDARY_OFFSET - cxQIX))  # Movement -> Southwest
                        dyQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[1] + QIX_BOUNDARY_OFFSET - cyQIX))
                elif x == 3:
                    if direction_limit in ["nord", "ouest"]:
                        dxQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[0] - QIX_BOUNDARY_OFFSET - cxQIX))  # Movement -> Northwest
                        dyQIX = round(max(-sin(pi/4)*depQIX, coin_sup_gauche[1] - QIX_BOUNDARY_OFFSET - cyQIX))
                    elif direction_limit in ["sud", "est"]:
                        dxQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[0] + QIX_BOUNDARY_OFFSET - cxQIX))   # Movement -> Southeast
                        dyQIX = round(min(sin(pi/4)*depQIX, coin_inf_droite[1] + QIX_BOUNDARY_OFFSET - cyQIX))
                if cxQIX + dxQIX > coin_inf_droite[0] or cxQIX + dxQIX < coin_sup_gauche[0] or cyQIX + dyQIX > coin_inf_droite[1] or cyQIX + dyQIX < coin_sup_gauche[1] :
                    break
                
                if dxQIX != 0 or dyQIX != 0 :
                    if test_interieur_safezone([lst_coordonnees_safezone],cxQIX,cyQIX):
                        cxQIX += -dxQIX
                        cyQIX += -dyQIX
                        efface("QIX")
                        draw_square(cxQIX - options['QIXSize'] / 2, cyQIX - options['QIXSize'] / 2, options['QIXSize'],"Red","Red","QIX")

                    else :
                        cxQIX += dxQIX
                        cyQIX += dyQIX
                        efface("QIX")
                        draw_square(cxQIX - options['QIXSize'] / 2, cyQIX - options['QIXSize'] / 2, options['QIXSize'],"Red","Red","QIX")


        dxSparx1, dySparx1 = 0, 0
        dxSparx1, dySparx1, last_sparx1_direction = mouvement_sparx(
            cxSparx1,
            cySparx1,
            True,
            last_sparx1_direction,
            coin_sup_gauche, 
            coin_inf_droite,
            depSparx
        )
        cxSparx1 += dxSparx1
        cySparx1 += dySparx1

        dxSparx2, dySparx2, last_sparx2_direction = mouvement_sparx(
            cxSparx2,
            cySparx2,
            False,
            last_sparx2_direction,
            coin_sup_gauche, 
            coin_inf_droite,
            depSparx
        )
        cxSparx2 += dxSparx2
        cySparx2 += dySparx2


        efface("Sparx")
        draw_sparx(cxSparx1, cySparx1)
        draw_sparx(cxSparx2, cySparx2)


#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
#   *                              Joueur                               *
#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *


        # Player movement input handling
        ev = donne_ev()
        tev = type_ev(ev)
        dx: float = 0
        dy: float = 0

        # Directional movement
        if touche_pressee(keys['gauche1']):
            dx = max(-dep, coin_sup_gauche[0] - cx)
        elif touche_pressee(keys['droite1']):
            dx = min(dep, coin_inf_droite[0] - cx)
        elif touche_pressee(keys['bas1']):
            dy = min(dep, coin_inf_droite[1] - cy)
        elif touche_pressee(keys['monter1']):
            dy = max(-dep, coin_sup_gauche[1] - cy)
        
        # Speed control (if variant enabled)
        if touche_pressee(keys['rapide1']) and "Vitesse" in lst_variantes:
            if coordonnees_debut is None:  # Toggle for drawing mode
                dep = options['vitRap']
                draw_status(1)
                dessiner = True
        
        if touche_pressee(keys['lent1']):
            if coordonnees_debut is None:
                dep = options['vitLent']
                draw_status(2)
                dessiner = True

        # Process player movement
        if dx != 0 or dy != 0:
            efface('curseur')
            
            # Test for collision with QIX - fix: use center coordinates and correct size
            perdu = test_perte(
                coordonnees_debut, # type: ignore
                (cx + dx, cy + dy),
                (cxQIX, cyQIX),  # Use center coordinates, not offset
                options['QIXSize'],  # Use QIX size, not capture area
                lst_coordonnees_curseur
            )

            cx += dx
            cy += dy

            # Obstacle collision detection
            if lst_obstacles is not None:
                for obstacle_pos in lst_obstacles:
                    if (encadrement_deux_sens(obstacle_pos[0], cx, obstacle_pos[0] + 10) and 
                        encadrement_deux_sens(obstacle_pos[1], cy, obstacle_pos[1] + 10)):
                        cx = cx - dx
                        cy = cy - dy
                        obstacle = True
                        break

            
            # Drawing logic when not hitting obstacles
            if dessiner and not obstacle:
                if coordonnees_debut is None:  # Test if player is on border
                    # Test if player exits safe zone
                    coordonnees_debut = test_sortie_safezone(
                        lst_coordonnees_safezone, cx, cy, dx, dy, dep
                    )
                    
                    if coordonnees_debut is not None:
                        # Test if player moves toward game zone
                        if test_interieur_safezone([lst_coordonnees_safezone], cx, cy):
                            ligne(cx - dx, cy - dy, cx, cy, "Gold", tag="Trainée")
                            lst_coordonnees_curseur.append((cx, cy))
                        else:  # Cancel movement if not going toward game zone
                            cx = cx - dx
                            cy = cy - dy
                            coordonnees_debut = None
                else:
                    lst_coordonnees_curseur.append((cx, cy))
                    ligne(cx - dx, cy - dy, cx, cy, "Gold", tag = "Trainée")
                    if perdu == True :
                        pass
                    elif test_entree_safezone(lst_coordonnees_safezone,int(cx),int(cy)) :       # Test pour savoir si le joueur entre dans la safezone
                        lst_coordonnees_curseur.insert(0, coordonnees_debut)        # Insertion de la première coordonnée du polygone formé par le joueur
                        lst_coordonnees_curseur = sommets(lst_coordonnees_curseur)  # Fonction pour réduire le nombre de coordonnées dans lst_coordonnees_curseur
                        lst_coordonnees_curseur = cw_a_ccw(lst_coordonnees_curseur) # Fonction pour faire en sorte que les coordonnées du polygone formé par le joueur soit dans le sens contraine de l'aiguille d'une montre (ccw)
                        lst_coordonnees_safezone, coordonnees_supprime = concatenation_safezone(lst_coordonnees_safezone, lst_coordonnees_curseur)  # Ajout et suppression des coordonnées de la safezone

                        if coordonnees_supprime is not None:  # Preserve previously drawn polygons
                            lst_coordonnees_curseur = lst_coordonnees_curseur + coordonnees_supprime

                        # Zone capture logic with error handling
                        try:
                            couleur = "green" if dep == options['vitRap'] else "dark blue"

                            # Check if QIX is inside the captured zone
                            if test_interieur_safezone([lst_coordonnees_safezone], cxQIX, cyQIX):
                                polygone(lst_coordonnees_curseur, "white", couleur, tag="ZoneC")
                                lst_coordonnees_polygones.append(lst_coordonnees_curseur)
                            else:
                                polygone(lst_coordonnees_safezone, "white", couleur, tag="ZoneC")
                                lst_coordonnees_polygones.append(lst_coordonnees_safezone)
                                lst_coordonnees_safezone = list(lst_coordonnees_curseur)

                            lst_coordonnees_safezone, coordonnees_debut_safezone = debut_egal_fin(
                                lst_coordonnees_safezone, coordonnees_debut_safezone
                            )
                            lst_coordonnees_safezone = sommets(lst_coordonnees_safezone)

                            # Calculate area with error handling
                            safe_zone_area = aire(lst_coordonnees_safezone, True)
                            if zonemax > 0:  # Prevent division by zero
                                zonetot = ((zonemax - safe_zone_area) / zonemax) * 100
                            else:
                                zonetot = 0
                                
                            # Update score
                            if score is not None:
                                efface("score")
                                area_bonus = safe_zone_area * (15 - float(dep))
                                score = score + int(area_bonus // 10000)
                                
                        except (ZeroDivisionError, ValueError) as e:
                            print(f"Error in zone calculation: {e}")
                            zonetot = 0
                            
                        # Clean up display
                        efface("Trainée")
                        if lst_obstacles is not None:
                            efface("obstacles")
                            for obstacle_pos in lst_obstacles:
                                draw_square(obstacle_pos[0], obstacle_pos[1], 10, "orange", "orange", "obstacles", 1)
                        
                        # Reset drawing state
                        efface("Zonecapturee")
                        lst_coordonnees_curseur = []
                        coordonnees_debut = None
                        coordonnees_supprime = None
                        perdu = False
                        update_action(zonetot, score)
            draw_player(cx, cy, rayon)
            obstacle = False





        # Sparx collision detection with player
        sparx_positions = [(cxSparx1, cySparx1), (cxSparx2, cySparx2)]
        for sparx_x, sparx_y in sparx_positions:
            if (encadrement_deux_sens(sparx_x - COLLISION_TOLERANCE, cx, sparx_x + COLLISION_TOLERANCE, True, True) and 
                encadrement_deux_sens(sparx_y - COLLISION_TOLERANCE, cy, sparx_y + COLLISION_TOLERANCE, True, True)):
                perdu = True
                break


        if tev == "Quitte" :
            return


        mise_a_jour()





#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
#   *                        Défaite / Victoire                         *
#   * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - *
    
        if zonetot >= zone_a_capture:
            niveau += 1
            show_level_complete(niveau)

            efface('curseur')
            cx, cy = WIDTH / 2, coin_inf_droite[1]
            draw_player(cx, cy, rayon)

            if "Obstacles" in lst_variantes:
                efface("obstacles")
                lst_obstacles = creation_obstacles(options['obstacles'], coin_sup_gauche, coin_inf_droite)

            # Level progression - increase difficulty
            if niveau % options['aCapt+'] == 0:
                zone_a_capture += options['aCapt+']

            # Reset and upgrade Sparx
            efface("Sparx")
            depSparx += options['vitSp+']
            cxSparx1, cxSparx2 = WIDTH / 2, WIDTH / 2
            cySparx1, cySparx2 = coin_sup_gauche[1], coin_sup_gauche[1]
            draw_sparx(cxSparx1, cySparx1)
            draw_sparx(cxSparx2, cySparx2)

            # Reset and upgrade QIX
            efface("QIX")
            depQIX += options['vitQIX+']
            cxQIX = WIDTH / 2
            cyQIX = (coin_inf_droite[1] - coin_sup_gauche[1]) / 4 + coin_sup_gauche[1]
            draw_square(cxQIX - QIX_SIZE_HALF, cyQIX - QIX_SIZE_HALF, 
                       options['QIXSize'], "Red", "Red", "QIX")

            zonetot = 0
            efface("Zonecapturee")
            efface("nbVies")
            efface("Zone_a_capturee")
            efface("niveau")
            efface("score")
            update_action(zonetot, score)
            update_round(zone_a_capture, nbVies, niveau)

            efface("ZoneC")
        
            dessiner = False
            lst_coordonnees_curseur = []
            coordonnees_debut = None
            coordonnees_debut_safezone = [
                (coin_inf_droite[0], coin_sup_gauche[1]),
                (coin_sup_gauche[0], coin_sup_gauche[1])
            ]
            lst_coordonnees_safezone = [
                (coin_inf_droite[0], coin_sup_gauche[1]),
                (coin_sup_gauche[0], coin_sup_gauche[1]),
                (coin_sup_gauche[0], coin_inf_droite[1]),
                (coin_inf_droite[0], coin_inf_droite[1]),
                (coin_inf_droite[0], coin_sup_gauche[1]),
                (coin_sup_gauche[0], coin_sup_gauche[1])
            ]
            lst_coordonnees_polygones = [
                [
                    (coin_sup_gauche[0], coin_sup_gauche[1]),
                    (coin_inf_droite[0], coin_sup_gauche[1]),
                    (coin_inf_droite[0], coin_inf_droite[1]),
                    (coin_sup_gauche[0], coin_inf_droite[1])
                ]
            ]


        if perdu:
            nbVies -= 1
            show_game_over(nbVies)

            efface('curseur')
            if coordonnees_debut is not None:
                cx, cy = coordonnees_debut[0], coordonnees_debut[1]
            draw_player(cx, cy, rayon)

            # Reset Sparx positions
            efface("Sparx")
            cxSparx1, cxSparx2 = WIDTH / 2, WIDTH / 2
            cySparx1, cySparx2 = coin_sup_gauche[1], coin_sup_gauche[1]
            draw_sparx(cxSparx1, cySparx1)
            draw_sparx(cxSparx2, cySparx2)


            # Update game state display
            efface("nbVies")
            update_round(zone_a_capture, nbVies, niveau)
            draw_status(0)
            dep = 6.0

            # Reset game state
            dessiner = False
            lst_coordonnees_curseur = []
            coordonnees_debut = None
            perdu = False

            # End game if no lives remaining
            if nbVies == 0:
                break
    
        a += 1


    ferme_fenetre()

if __name__ == "__main__" :

    main()