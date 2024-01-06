========= Bonus implémentés =========
- Niveaux : à chaque fois que le joueur capture plus de 75%, la zone de jeu redevient vierge et la vitesse des ennemis augmente.

- Scores : le score est bien affiché constamment et se met à jour correctement. De plus, il y un affichage différent lorsque le jeu est joué avec deux joueurs, avec les informations des joueurs d'affichés sur les côtés de la zone de jeu, dans un cadre. Les informations relatives aux joueurs sont alors : le pourcentage de zone capturé, le statut du stylo/dessin (ne trace pas/vitesse normale/vitesse lente), et il y aura aussi par la suite les vies.

- Obstacles : des obstacles sont générés aléatoirement dans la zone de jeu.

- Deux Joueurs : deux joueurs peuvent jouer en même temps, l'un avec ZQSD et A/E (pour la vitesse de déplacement), et l'autre avec ↑←↓→ et Right Crtl/Right Shift. Tout ce qui était prévu pour ce bonus n'a pas encore été totalement ajouté au jeu (vies séparées par exemple) par manque de temps.

- Vitesse : en appuyant sur une touche (dépendante du joueur), le joueur a possibilité de changer de vitesse de déplacement. Une vitesse plus lente permet d'obtenir un score plus élevé. De plus, il n'est possible de changer de vitesse que lorsque le joueur se trouve sur un trait déjà construit (bordure ou polygone).

~ Niveaux (un peu présent) : à la fin de chaque niveau, la vitesse des ennemis augmente, et tous les 5 niveaux, il faut capturer 1% de zone totale en plus pour gagner. Pour le reste, nous n'avons pas eu le temps de le faire, mais nous avons des idées de comment faire (par exemple, pour les sparxs, en rajouter un tous les 5 niveaux, dont le sens de déplacement alternera. Cela peut se faire avec, notamment, les dictionnaires (nous n'avons pas pu le faire dans la première phase comme nous ne connaissions pas ce type).

X Bonus : Les bonus ne sont pas présents, encore une fois par manque de temps. Les pommes (3) seront générées aléatoirement dans la zone de jeu, comme dans le jeu Snake. Celles-ci seront représentées par une image de pomme (dans le même style que le coeur symbolisant les vies), avec une hitbox carrée de taille correspondante à l'image affichée. Le temps d'invincibilité serait géré avec le module 'time'.

X Sparx "internes" : Encore et toujours, cette variante n'a pas été implémentée à cause des délais. Cependant, le fonctionnement de la fonction est déjà posé, il ne reste plus qu'à le coder (voir plus bas pour avoir un descriptif de comment la fonction marcherait).
        [PS : Pour les sparx, cela est de ma faute, j'étais celui qui devait m'en occuper, mais en ayant déjà eu du mal à faire des sparx semi-fonctionnels pour le premier rendu, j'ai préféré m'occuper d'autres éléments que j'étais sûr de savoir faire avant, afin de ne pas perdre trop de temps (alors que celui-ci est déjà très limité). - Romain]


========= Organisation du programme =========
Le programme est composé de 3 fichiers de code :
- Le fichier Interface, qui contient les fonctions destinés aux éléments visibles à l'écran (zone de jeu, entités, score, ...);
- Le fichier Calculs, qui contient la majorité des fonctions destinés à calculer différentes données;
- Le fichier Gameplay, qui contient le code principal. C'est là que les mouvements, les zones, les différents comportements sont définis.



========= Choix Techniques =========
> Pour la safezone, on a décidé de faire en sorte que ça soit que la bordure de la zone de jeu pour nous simplifier le calcul de l'aire (l'aire de la zone de jeu initiale - l'aire de la safezone).

> Pour le calcul de l'aire, j'ai cherché sur Internet une manière de calculer l'aire d'un polygone à l'aide des coordonnées de ses sommets et j'ai trouvé cette solution.

> Pour la fonction sommets, je me suis dit que cette fonction augmenterait énormément la performance du jeu (à la place de garder en mémoire toutes les coordonnées de chaque point d'un segment, on peut juste garder en mémoire les coordonnées des sommets).

> Pour la fonction concatenation_safezone, on avait eu plusieurs idées, mais les idées précédant la fonction actuelle ne fonctionnaient pas toujours, et donc j'ai vu qu'à chaque fois que l'on capture une zone, soit :
- Le début et la fin de la zone capturée est entre 2 points de la safezone,
- Le début de la zone capturée est entre 2 points de la safezone mais la fin ne l'est pas et donc, tant que la fin n'est pas entre 2 points de la safezone, il faut les supprimer.
Les coordonnées de la safezone qui sont supprimées doivent être renversées car sinon, le polygone ne serait pas dans le bon ordre.

> La fonction debut_egal_fin n'est utile que pour les extrémités du polygone car, sans cette fonction, il faudrait rajouter, à chaque fonction utilisant l'index i+1 à la safezone, la condition qui vérifie si l'index == len((liste) - 1) ce qui doublerait la taille du code.

> Pour les sparxs (ceci n'est pas encore implémenté), nous sommes partis sur une idée totalement différente de la première, qui était alors temporaire (l'ancienne idée pouvait être la plus instinctive). Ce changement a été fait car la fonction n'était déjà fonctionnelle qu'à moitié (le sens horaire fonctionnait, le sens anti-horaire non) et surtout, beaucoup trop longue (+300 lignes). 
La (future) nouvelle version vérifiera si les coordonnées actuelles du sparx se trouvent dans lst_coordonnées_polygones (qui contient les sommets de la zone de jeu, ainsi que des différents polygones formés par le(s) joueur(s)). Si les coordonnées s'y trouvent, il regardera alors le prochain couple (ou celui d'avant, en fonction du sens dans lequel tourne le sparx) et se dirigera vers ce prochain point. Si les coordonnées du sparx se trouve dans une autre liste alors que celui-ci est déjà dans une, un chiffre aléatoire sera tiré, et en fonction du résultat, il changera (ou non) de chemin (ce sera la même probabilité pour chaque chemin).
Cette méthode devrait permettre le mouvement du sparx auteur de la zone capturée par le joueur, ainsi que les déplacements internes.

> Pour le menu, on est allé pour un qui est simple pour ne pas trop ajouter trop de travail (avec les autres SAEs, TPs, etc). On s'est dit qu'il était possible de faire une fonction pour faire les boîtes avec du texte à l'intérieur mais il y aurait eu beaucoup de variables à mettre et on a décidé de juste copier coller le code (malgré la longueur des fonctions).


========= Problèmes Rencontrés =========
- Certaines fonctions, comme debut_egal_fin ou concatenation_safezone, ne fonctionnent pas dans 100% des situations, et on n'arrive pas à trouver la source des problèmes. 
Ainsi, l'utilisation de ces fonctions peut entraîner des problèmes sur certains passages qui les utilisent (par exemple, pour les Sparx)

- Pour le mouvement des Sparx, notamment pour les raisons d'au-dessus

- Limite de temps : bien que le jeu semble simple, en théorie, à coder, certaines choses sont difficiles à implémenter dans les faits, et cela peut être une vraie source
de perte de temps. De plus, le temps pendant lequel on peut travailler sur le projet est très court, et cela est d'autant plus vrai en cette période de fin de semestre, où s'entremêlent plein de projets et de devoirs qui prennent, eux aussi, du temps (notamment lorsqu'on nous donne un nouveau projet il y a à peine 2 semaines, ce qui fait un peu tard pour ne pas mentir). Les bugs que l'on découvre au fur et à mesure prennent également du temps à résoudre, et devoir ajouter toutes les variantes resserre encore le délai déjà initialement serré, résultant dans le fait que certaines choses soient manquantes.

[Romain : Cela est d'autant plus vrai pour moi, qui suis moins à l'aise sur Python que Jérémy... Ce n'est pas faute d'essayer, j'ai passé, sans aucun doute, plus de 70H à coder, ou en tout cas à essayer, pour n'avoir que peu de résultats; la "seule" chose pour laquelle ma contribution est visible est pour l'aspect graphique du jeu (interface et ce qui lui est lié)
C'est ce genre de choses, qui sont normalement simple à faire mais avec lesquelles j'ai du mal, qui me donnent une réel sensation de n'être qu'un poids mort pour mon binôme]
