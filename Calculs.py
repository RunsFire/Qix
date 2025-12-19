import doctest
from typing import List, Tuple, Optional


def aire(lst: List[Tuple[float, float]], positif=True) -> float :                # Pas 100% sur que ça marche toujours
    """Calculate the area of a polygon defined by its vertices.

    Args:
      lst: List of (x, y) tuples representing the polygon's vertices.
      positif: If True, returns the absolute value of the area (default True).

    Returns:
      The area of the polygon as a float.

    Raises:
      AssertionError: If the input list is empty.

    Examples:
      >>> aire([[2,2],[4,2],[4,4],[2,4]], True)
      4.0
      >>> aire([[4,2],[2,2],[2,4],[4,4],[4,2],[2,2]], False)
      -4.0
      >>> aire([[2,2],[3,2],[4,2],[4,3],[4,4],[3,4],[2,4]], False)
      4.0
      >>> aire([], True)
      Traceback (most recent call last):
        ...
      AssertionError
      >>> aire([[1,1],[2,2]], True)
      0.0
      >>> aire([[0,0],[2,0],[2,2],[1,2],[1,3],[3,3],[3,2],[4,2],[4,4],[0,4]], True)
      10.0
    """
    assert lst != []
    aire = 0
    lst0 = list(lst[0])
    lst_precedent = lst[0]
    aire += lst0[0] * lst_precedent[1] - lst0[1] * lst_precedent[0]
    for element in lst :
        aire += lst_precedent[0] * element[1] - lst_precedent[1] * element[0]
        lst_precedent = element
    lstn = list(lst[len(lst)-1])
    aire += lstn[0] * lst0[1] - lstn[1] * lst0[0]
    if aire < 0 and positif :               # Si l'aire est négative c'est parce que les coordonnées des points du polygone sont listés dans le sens d'une aiguille d'une montre
        aire *= -1                          # Cette ligne permet de toujours avoir une aire positive si voulu.
    return aire/2





def sommets(lst: List[Tuple[float, float]]) -> List[Tuple[float, float]] :
    """Extract the vertices from a list of coordinate points.

    Args:
      lst: List of (x, y) tuples representing coordinate points.

    Returns:
      A list of (x, y) tuples representing the vertices of the polygon.

    Raises:
      AssertionError: If the input list is empty.

    Examples:
      >>> lst = [(500.0, 795), (500.0, 770), (500.0, 765), (475.0, 765), (470.0, 765), (470.0, 760), (475.0, 760), (475.0, 755), (470.0, 755), (470.0, 750), (470.0, 725), (490.0, 725), (495.0, 725), (495.0, 730), (495.0, 735), (495.0, 740)]
      >>> sommets(lst)
      [(500.0, 795), (500.0, 765), (470.0, 765), (470.0, 760), (475.0, 760), (475.0, 755), (470.0, 755), (470.0, 725), (495.0, 725), (495.0, 740)]
      >>> sommets([])
      Traceback (most recent call last):
        ...
      AssertionError
      >>> sommets([(195, 800)])
      [(195, 800)]
      >>> sommets([(195, 800), (200, 800)])
      [(195, 800), (200, 800)]
    """
    assert lst != []
    if len(lst) <= 2 :
        return lst
    lst_sommets = [lst[0]]
    coordonnee2 = lst[0]
    coordonnee1 = lst[1]
    i = 0
    for element in lst :
        if (element[0] == coordonnee1[0] and element[0] == coordonnee2[0]) or (element[1] == coordonnee1[1] and element[1] == coordonnee2[1]):
            if i % 2 == 0 :
                coordonnee2 = element
            else :
                coordonnee1 = element
        else :
            if i % 2 == 0 :
                lst_sommets.append(coordonnee1)
                coordonnee2 = element
            else :
                lst_sommets.append(coordonnee2)
                coordonnee1 = element
        if i == len(lst)-1 :
            lst_sommets.append(element)
        i += 1
    return lst_sommets






def encadrement(element1: float, element2: float, element3: float, egal1=True, egal2=True) -> bool :
    """Check if element2 is between element1 and element3.

    Args:
      element1: First boundary element.
      element2: Element to check if it's within bounds.
      element3: Second boundary element.
      egal1: If True, includes equality for the first comparison (default True).
      egal2: If True, includes equality for the second comparison (default True).

    Returns:
      True if element2 is between element1 and element3, False otherwise.

    Examples:
      >>> encadrement(2,2,2,True,True)
      True
      >>> encadrement(2,2,2,False,True)
      False
      >>> encadrement(1,2,3,False,False)
      True
      >>> encadrement(2,2,3,True,False)
      True
    """
    if egal1:
        resultat1 = element1 <= element2
    else :
        resultat1 = element1 < element2
    if egal2:
        resultat2 = element2 <= element3
    else :
        resultat2 = element2 < element3
        
    return resultat1 and resultat2






def encadrement_deux_sens(element1: float, element2: float, element3: float, egal1=True, egal2=True) -> bool :
    """Check if element2 is between element1 and element3 in both directions.

    Performs the encadrement check in both directions: 
    (element1 < element2 < element3) or (element3 < element2 < element1).

    Args:
      element1: First boundary element.
      element2: Element to check if it's within bounds.
      element3: Second boundary element.
      egal1: If True, includes equality for the first comparison (default True).
      egal2: If True, includes equality for the second comparison (default True).

    Returns:
      True if element2 is between element1 and element3 in either direction, False otherwise."""
    return encadrement(element1,element2,element3,egal1,egal2) or encadrement(element3,element2,element1,egal1,egal2)






def cw_a_ccw(M: List[Tuple[float, float]]) -> List[Tuple[float, float]] :
    """Convert coordinate matrix from clockwise to counter-clockwise orientation.

    Takes a matrix of coordinates and ensures they are ordered counter-clockwise.
    If the coordinates are already counter-clockwise, returns them unchanged.
    If they are clockwise, reverses the order.

    Args:
      M: List of (x, y) tuples representing polygon vertices.

    Returns:
      List of (x, y) tuples in counter-clockwise order.

    Raises:
      AssertionError: If the input list has exactly one element.

    Examples:
      >>> cw_a_ccw([(2,2),(4,2),(4,4),(2,4)])
      [(2, 2), (4, 2), (4, 4), (2, 4)]
      >>> cw_a_ccw([(2,2),(2,4),(4,4),(4,2)])
      [(4, 2), (4, 4), (2, 4), (2, 2)]
      >>> M = [(2,2),(4,2),(4,4),(2,4)]
      >>> cw_a_ccw(M)
      [(2, 2), (4, 2), (4, 4), (2, 4)]
      >>> cw_a_ccw([(800,150),(200,150)])
      [(200, 150), (800, 150)]
      >>> cw_a_ccw([(300,450),(300,800)])
      [(300, 450), (300, 800)]
    """
    assert len(M) != 1
    if len(M) == 2 :
        if M[0][0] == M[1][0] :
            if M[0][1] > M[1][1] :
                M.reverse()
        else :
            if M[0][0] > M[1][0] :
                M.reverse()
    elif aire(M,False) < 0 :
        M.reverse()
    return M
    



def concatenation_safezone(lst_safezone: List[Tuple[float, float]], zone_capturee: List[Tuple[float, float]]) -> Tuple[List[Tuple[float, float]], Optional[List[Tuple[float, float]]]] :   # Does not work for all cases yet and is the reason the game sometimes crashes
    """Merge captured zone coordinates into the safezone coordinates.

    Returns a matrix with the coordinates of zone_capturee inserted into lst_safezone.
    Removes coordinates if necessary. The counter-clockwise direction is required
    for the zone_capturee matrix.

    Args:
      lst_safezone: List of (x, y) tuples representing the current safe zone boundary.
      zone_capturee: List of (x, y) tuples representing the newly captured zone.

    Returns:
      A tuple containing:
        - The updated safezone coordinates as a list of (x, y) tuples
        - The removed vertices as a list of (x, y) tuples, or None if no vertices were removed

    Raises:
      ValueError: If the captured zone coordinates don't correspond to the safezone.
    """
    sommets_supprime = []
    for i in range (len(lst_safezone) - 1) :

        if ((zone_capturee[0][0] == lst_safezone[i][0] and zone_capturee[0][0] != zone_capturee[-1][0]    # Vérifie si le 1er point de la zone capturée
        and  encadrement_deux_sens(lst_safezone[i][1],zone_capturee[0][1],lst_safezone[i+1][1],True,True))                  # n'est pas sur la même ligne de la safezone
        or  (zone_capturee[0][1] != zone_capturee[-1][1] and zone_capturee[0][1] == lst_safezone[i][1]    # que le dernier
        and  encadrement_deux_sens(lst_safezone[i][0],zone_capturee[0][0],lst_safezone[i+1][0],True,True))) :               # (avec coordonnées x et y)
            while True :
                if (lst_safezone[i+1][0] == zone_capturee[-1][0] or lst_safezone[i+1][1] == zone_capturee[-1][1]) :
                    sommets_supprime.append(lst_safezone.pop(i+1))
                    break
                else :
                    sommets_supprime.append(lst_safezone.pop(i+1))
            sommets_supprime.reverse()                                                  # Pour que la liste des coordonnées soit dans le bon sens
            lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]      # Insertion des éléments de la zone_capturee dans lst_safezone
            return (lst_safezone, sommets_supprime)
        

        elif zone_capturee[0] == lst_safezone[i] == zone_capturee[-1] :
            lst_safezone.pop(i)
            lst_safezone = lst_safezone[:i+1] + zone_capturee[1:] + lst_safezone[i+1:]
            return (lst_safezone, None)




        elif zone_capturee[0][0] == lst_safezone[i][0] :        # Vérifie si le premier x de la zone capturée appartient à la safezone
            if encadrement_deux_sens(lst_safezone[i][1],zone_capturee[0][1],lst_safezone[i+1][1],False,False) :     # Test pour savoir si le y du premier élément de zone_capturee est entre 2 coordonnées de lst_safezone
                if (encadrement_deux_sens(lst_safezone[i][1],zone_capturee[-1][1],lst_safezone[i+1][1],False,False  # Même test mais pour le dernier élément
                and zone_capturee[-1][0] == lst_safezone[i][0])):
                    lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]
                    return (lst_safezone, None)
                else :
                    while True :
                        sommets_supprime.append(lst_safezone.pop(i+1))
                        if lst_safezone[i+1][0] == zone_capturee[-1][0] or lst_safezone[i+1][1] == zone_capturee[-1][1] :
                            sommets_supprime.append(lst_safezone.pop(i+1))
                            break
                sommets_supprime.reverse()
                lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]
                return (lst_safezone, sommets_supprime)




        elif zone_capturee[0][1] == lst_safezone[i][1] :        # Vérifie si le premier y de la zone capturée appartient à la safezone (identique au bloc précédent)
            if encadrement_deux_sens(lst_safezone[i][0],zone_capturee[0][0],lst_safezone[i+1][0],False,False) :
                if (encadrement_deux_sens(lst_safezone[i][0],zone_capturee[-1][0],lst_safezone[i+1][0],False,False)
                and zone_capturee[-1][1] == lst_safezone[i][1]):
                    lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]
                    return (lst_safezone, None)
                else :
                    while True :
                        sommets_supprime.append(lst_safezone.pop(i+1))
                        if lst_safezone[i+1][0] == zone_capturee[-1][0] or lst_safezone[i+1][1] == zone_capturee[-1][1] :
                            sommets_supprime.append(lst_safezone.pop(i+1))
                            break
                sommets_supprime.reverse()
                lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]
                return (lst_safezone, sommets_supprime)
    
    raise ValueError("The captured zone coordinates do not correspond to the safezone.")







def debut_egal_fin(lst_safezone: List[Tuple[float, float]] , debut_safezone: List[Tuple[float, float]]) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]] :       # Does not always work
    """Ensure the first two elements match the last two elements in the safezone.

    Returns lst_safezone with the first 2 elements in the same arrangement as the
    last 2 elements. debut_safezone helps track which coordinates have changed
    and modify the necessary coordinates.

    Args:
      lst_safezone: List of (x, y) tuples representing the safezone boundary.
      debut_safezone: List of (x, y) tuples representing the initial safezone state.

    Returns:
      A tuple containing:
        - The updated safezone coordinates as a list of (x, y) tuples
        - The updated debut_safezone coordinates as a list of (x, y) tuples
    """
    lst_safezone_copie = list(lst_safezone)

    if [lst_safezone[0],lst_safezone[1]] != debut_safezone and [lst_safezone[len(lst_safezone)-2],lst_safezone[len(lst_safezone)-1]] != debut_safezone :
        lst_safezone_copie.insert(0,lst_safezone[len(lst_safezone)-1])
        lst_safezone_copie.append(lst_safezone[0])
        debut_safezone = [lst_safezone[len(lst_safezone)-1],lst_safezone[0]]
        return lst_safezone_copie, debut_safezone

    elif [lst_safezone[0],lst_safezone[1]] != debut_safezone :
        debut_safezone = [lst_safezone[0],lst_safezone[1]]
        lst_safezone[len(lst_safezone)-2], lst_safezone[len(lst_safezone)-1] = debut_safezone[0], debut_safezone[1]

    elif [lst_safezone[len(lst_safezone)-2],lst_safezone[len(lst_safezone)-1]] != debut_safezone :
        debut_safezone = [lst_safezone[len(lst_safezone)-2], lst_safezone[len(lst_safezone)-1]]
        lst_safezone[0], lst_safezone[1] = debut_safezone[0], debut_safezone[1]
        
    return lst_safezone, debut_safezone






if __name__ == "__main__" :
    doctest.testmod()