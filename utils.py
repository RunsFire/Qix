from typing import Tuple, List, Optional
from Interface.utils import draw_square, cercle
from Calculs import encadrement_deux_sens
import random



def test_perte(
        cd_debut: Optional[Tuple[float, float]],
        cd_joueur: Tuple[float, float],
        cd_QIX: Tuple[float, float],
        qix_size: float,
        lst_joueur: List[Tuple[float, float]],
        is_immobile: bool
    ) -> bool:
    """
    Test if the player loses due to collision with QIX or self-intersection.
    
    Args:
        cd_debut: Starting coordinates of player trail
        cd_joueur: Current player coordinates  
        cd_QIX: QIX center coordinates
        qix_size: QIX size (width/height)
        lst_joueur: List of player trail coordinates
        is_immobile: Whether the player is currently immobile
        
    Returns:
        True if collision detected, False otherwise
    """
    # Player is on safe zone
    if cd_debut is None:
        return False

    # Check if player returned to starting position
    if cd_debut == cd_joueur:
        return True
    
    qix_left = cd_QIX[0] - qix_size / 2
    qix_right = cd_QIX[0] + qix_size / 2
    qix_top = cd_QIX[1] - qix_size / 2
    qix_bottom = cd_QIX[1] + qix_size / 2

    # Check QIX collision with trail and self-intersection
    for i, element in enumerate(lst_joueur):
        # Check if QIX collides with any trail point
        if (qix_left <= element[0] <= qix_right and 
            qix_top <= element[1] <= qix_bottom):
            return True
        # Check for self-intersection
        if cd_joueur == element:
            # Allow last point if player is immobile
            return not (is_immobile and i == len(lst_joueur) - 1)
            
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


def test_interieur_safezone(game_boundary: List[Tuple[float, float]], cx: float, cy: float) -> bool:
    """
    Test if a point is inside the current game boundary (unsafe area).
    
    Instead of checking multiple safe zone polygons, this optimized version checks
    if the point is inside the single game boundary polygon representing the 
    current unsafe area where the QIX can move.
    
    Args:
        game_boundary: List of (x, y) coordinates defining the current game boundary
        cx: Point x-coordinate to test
        cy: Point y-coordinate to test
        
    Returns:
        True if point is inside the game boundary (unsafe area), False otherwise
    """
    return _point_in_polygon(game_boundary, cx, cy)



def _point_in_polygon(polygon: List[Tuple[float, float]], px: float, py: float) -> bool:
    """
    Optimized point-in-polygon test using ray casting algorithm.
    
    Args:
        polygon: List of (x, y) coordinates defining the polygon
        px: Point x-coordinate to test
        py: Point y-coordinate to test
        
    Returns:
        True if point is inside polygon, False otherwise
    """
    if not polygon or len(polygon) < 3:
        return False
    
    # Bounding box quick rejection test
    min_x = min(point[0] for point in polygon)
    max_x = max(point[0] for point in polygon) 
    min_y = min(point[1] for point in polygon)
    max_y = max(point[1] for point in polygon)
    
    if px < min_x or px > max_x or py < min_y or py > max_y:
        return False
    
    # Ray casting algorithm
    inside = False
    j = len(polygon) - 1  # Last vertex
    
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        # Check if ray crosses this edge
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        
        j = i  # Move to next edge
    
    return inside
    

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