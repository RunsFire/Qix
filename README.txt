========= Bonus implémentés =========
- Niveaux : à chaque fois que le joueur capture plus de 75%, la zone de jeu redevient vierge et la vitesse des ennemis augmente.
- Scores : il manque le nombre de points obtenus, mais le nombre de vies restantes et le pourcentage d'aire gagnée par le joueur sont affichés. (le style de l'interface est
très brut pour le moment, et sera amélioré par la suite).



========= Organisation du programme =========
Le programme est composé de 3 fichiers :
- Le fichier interface, qui contient les fonctions destinés aux éléments visibles à l'écran (zone de jeu, entités, scores, ...);
- Le fichier calculs, qui contient la majorité des fonctions destinés à calculer différentes données;
- Le fichier gameplay, qui contient le code principal. C'est là que les mouvements, les zones, les différents comportements sont définis.



========= Choix Techniques =========
Pour la safezone, on a décidé de faire en sorte que ça soit que la bordure de la zone de jeu pour nous simplifier le calcul de l'aire (l'aire de la zone de jeu initiale - l'aire de la safezone).
Pour le calcul de l'aire, j'ai cherché sur Internet une manière de calculer l'aire d'un polygone à l'aide des coordonnées de ses sommets et j'ai trouvé cette solution.
Pour la fonction sommets, je me suis dit que cette fonction augmenterait énormément la performance du jeu (à la place de garder en mémoire toutes les coordonnées de chaque point d'un segment, on peut juste garder en mémoire les coordonnées des sommets).
Pour la fonction concatenation_safezone, on avait eu plusieurs idées, mais les idées précédant la fonction actuelle ne fonctionnaient pas toujours, et donc j'ai vu qu'à chaque fois que l'on capture une zone, soit :
- Le début et la fin de la zone capturée est entre 2 points de la safezone,
- Le début de la zone capturée est entre 2 points de la safezone mais la fin ne l'est pas et donc, tant que la fin n'est pas entre 2 points de la safezone, il faut les supprimer.
Les coordonnées de la safezone qui sont supprimées doivent être renversées car sinon, le polygone ne serait pas dans le bon ordre.
La fonction debut_egal_fin n'est utile que pour les extrémités du polygone car, sans cette fonction, il faudrait rajouter, à chaque fonction utilisant l'index i+1 à la safezone, la condition qui vérifie si l'index == len((liste) - 1) ce qui doublerait la taille du code.


========= Problèmes Rencontrés =========
- Certaines fonctions, comme debut_egal_fin ou concatenation_safezone, ne fonctionnent pas dans 100% des situations, et on n'arrive pas à trouver la source des problèmes. 
Ainsi, l'utilisation de ces fonctions peut entraîner des problèmes sur certains passages qui les utilisent (par exemple, pour les Sparx)
- Pour le mouvement des Sparx, notamment pour les raisons d'au-dessus
- Limite de temps : bien que le jeu semble simple, en théorie, à coder, certaines choses sont difficiles à implémenter dans les faits, et cela peut être une vrai source
de perte de temps.
[Romain : Cela est d'autant plus vrai pour moi, qui suis moins à l'aise sur Python que Jérémy. J'ai dû passer plus de 60H pour avoir un Sparx qui fonctionne correctement, et encore, seul l'un des deux fonctionne bien ...
C'est ce genre de choses, qui sont normalement simple à faire mais avec lesquelles j'ai du mal, qui me donnent une réel sensation de n'être qu'un poids mort pour mon binôme]
