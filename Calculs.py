import doctest




def aire(lst, positif) :                # Pas 100% sur que ça marche toujours
    """ Renvoie l'aire d'un polygone ayant pour sommet (x,y) dans une liste lst. positif est un booleen qui permet de laisser ou pas une aire négative en retour.
    >>> aire([[2,2],[4,2],[4,4],[2,4]],True)
    4.0
    >>> aire([[4,2],[2,2],[2,4],[4,4],[4,2],[2,2]],False)
    -4.0
    >>> aire([[2,2],[3,2],[4,2],[4,3],[4,4],[3,4],[2,4]],False)
    4.0
    >>> aire([],True)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> aire([[1,1],[2,2]],True)
    0.0
    >>> aire([[0,0],[2,0],[2,2],[1,2],[1,3],[3,3],[3,2],[4,2],[4,4],[0,4]],True)
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






def sommets(lst) :
    """ Renvoie les coordonnées des sommets d'une liste de coordonnées de points
    >>> lst = [[500.0, 795], [500.0, 770], [500.0, 765], [475.0, 765], [470.0, 765], [470.0, 760], [475.0, 760], [475.0, 755], [470.0, 755], [470.0, 750], [470.0, 725], [490.0, 725], [495.0, 725], [495.0, 730], [495.0, 735], [495.0, 740]]
    >>> sommets(lst)
    [[500.0, 795], [500.0, 765], [470.0, 765], [470.0, 760], [475.0, 760], [475.0, 755], [470.0, 755], [470.0, 725], [495.0, 725], [495.0, 740]]
    >>> sommets([])
    Traceback (most recent call last):
        ...
    AssertionError
    >>> sommets([[195, 800]])
    [[195, 800]]
    >>> sommets([[195, 800], [200, 800]])
    [[195, 800], [200, 800]]
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






def encadrement(element1, element2, element3, egal1, egal2) :
    """Renvoie True si l'element2 est compris entre l'element1 et l'element3. egal est un bouléen qui rajoute l'égalité si besoin.
    >>> encadrement(2,2,2,True,True)
    True
    >>> encadrement(2,2,2,False,True)
    False
    >>> encadrement(1,2,3,False,False)
    True
    >>> encadrement(2,2,3,True,False)
    True
    """
    if egal1 == True :
            if egal2 == True :
                if element1 <= element2 and element2 <= element3 :
                    return True
                else :
                    return False
            else :
                if element1 <= element2 and element2 < element3 :
                    return True
                else :
                    return False
    elif egal2 == True :
        if element1 < element2 and element2 <= element3 :
            return True
        else :
            return False
    else :
        if element1 < element2 and element2 < element3 :
            return True
        else :
            return False






def encadrement_deux_sens(element1, element2, element3, egal1, egal2) :
    """Effectue l'encadrement de element2 dans les 2 sens (element1 < element2 < element3 ou element3 < element2 < element1)"""
    return encadrement(element1,element2,element3,egal1,egal2) or encadrement(element3,element2,element1,egal1,egal2)






def cw_a_ccw(M) :
    """Renvoie la matrice de coordonnées dans un sens (aiguille d'une montre (cw) ou contraire à l'aiguille d'une montre (ccw)) dans le sens contraire de l'aiguille d'une montre
    >>> cw_a_ccw([[2,2],[4,2],[4,4],[2,4]])
    [[2, 2], [4, 2], [4, 4], [2, 4]]
    >>> cw_a_ccw([[2,2],[2,4],[4,4],[4,2]])
    [[4, 2], [4, 4], [2, 4], [2, 2]]
    >>> M = [[2,2],[4,2],[4,4],[2,4]]
    >>> cw_a_ccw(M)
    [[2, 2], [4, 2], [4, 4], [2, 4]]
    >>> cw_a_ccw([[800,150],[200,150]])
    [[200, 150], [800, 150]]
    >>> cw_a_ccw([[300,450],[300,800]])
    [[300, 450], [300, 800]]
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
    




def concatenation_safezone(lst_safezone, zone_capturee) :   # Ne fonctionne pas pour tous les cas encore et est la raison que le jeu crash quelque fois
    """Renvoie une matrice avec les coordonnées de zone_capturee dans lst_safezone. Supprime des coordonnées si nécessaire.
       Le sens anti-horaire est nécessaire pour la matrice zone_capturee."""
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
       


        elif zone_capturee[0] == lst_safezone[i] :
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
                        if lst_safezone[i+1][0] == zone_capturee[len(zone_capturee)-1][0] or lst_safezone[i+1][1] == zone_capturee[len(zone_capturee)-1][1] :
                            sommets_supprime.append(lst_safezone.pop(i+1))
                            break
                sommets_supprime.reverse()
                lst_safezone = lst_safezone[:i+1] + zone_capturee + lst_safezone[i+1:]
                return (lst_safezone, sommets_supprime)







def debut_egal_fin(lst_safezone,debut_safezone) :       # Fonctionne pas toujours
    """Renvoie lst_safezone avec les 2 premiers éléments dans la même disposition que les 2 derniers éléments. debut_safezone permet de savoir quelles coordonnées ont changé et changer les coordonnées nécessaires."""
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
