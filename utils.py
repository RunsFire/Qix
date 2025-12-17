from typing import Tuple, List, Optional
from Interface.utils import draw_square, cercle
from Calculs import encadrement_deux_sens
import random



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