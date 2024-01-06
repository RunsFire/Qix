========= Bonus implémentés =========
- Niveaux : à chaque fois que le joueur capture plus de 75%, la zone de jeu redevient vierge et la vitesse des ennemis augmente.

- Scores : le score est bien affiché constamment et se met à jour correctement. De plus, il y un affichage différent lorsque le jeu est joué avec deux joueurs, avec les 
informations des joueurs d'affichés sur les côtés de la zone de jeu, dans un cadre. Les informations relatives aux joueurs sont alors : le pourcentage de zone capturé, 
le statut du stylo/dessin (ne trace pas/vitesse normale/vitesse lente), et il y aura aussi par la suite les vies.

- Obstacles : des obstacles sont générés aléatoirement dans la zone de jeu.

- Deux Joueurs : deux joueurs peuvent jouer en même temps, l'un avec ZQSD et A/E (pour la vitesse de déplacement), et l'autre avec ↑←↓→ et Right Crtl/Right Shift. Tout ce 
qui était prévu pour ce bonus n'a pas encore été totalement ajouté au jeu (vies séparées par exemple) par manque de temps.

- Vitesse : en appuyant sur une touche (dépendante du joueur), le joueur a possibilité de changer de vitesse de déplacement. Une vitesse plus lente permet d'obtenir un score 
plus élevé. De plus, il n'est possible de changer de vitesse que lorsque le joueur se trouve sur un trait déjà construit (bordure ou polygone).

- Niveaux : à la fin de chaque niveau, la vitesse des ennemis augmente, et tous les X niveaux (modifiable), il faut capturer X% de zone totale en plus pour gagner. 
Des Sparxs sont également ajoutés.

~ Bonus : Les bonus ne sont pas présents, encore une fois par manque de temps. Les pommes (3) seront générées aléatoirement dans la zone de jeu, comme dans le jeu Snake. 
Celles-ci seront représentées par une image de pomme (dans le même style que le coeur symbolisant les vies), avec une hitbox carrée de taille correspondante à l'image 
affichée. Le temps d'invincibilité serait géré avec le module 'time'.

X Sparx ("internes") : Malgré le temps passé sur ceux-ci, les sparx ne sont toujours pas fonctionnel (du moins pour le rendu, j'espère pouvoir régler le problème d'ici la 
soutenance, mais je ne promet rien). La cause de leur disfonctionnement a été repéré (cela provient des polygones formées, plus précisément de leurs coordonnées) et nous 
pensons avoir trouver d'où vient le problème (fonction de concatenation). Cependant, nous n'avons pas eu le temps de localiser précisément la source du problème dans le 
code pour le régler.


========= Organisation du programme =========
Le programme est composé de 3 fichiers de code :
- Le fichier Interface, qui contient les fonctions destinés aux éléments visibles à l'écran (zone de jeu, entités, score, ...);
- Le fichier Calculs, qui contient la majorité des fonctions destinés à calculer différentes données;
- Le fichier Gameplay, qui contient le code principal. C'est là que les mouvements, les zones, les différents comportements sont définis.



========= Choix Techniques =========
> Pour la safezone, on a décidé de faire en sorte que ça soit que la bordure de la zone de jeu pour nous simplifier le calcul de l'aire (l'aire de la zone de jeu initiale - l'aire de la safezone).

> Pour le calcul de l'aire, j'ai cherché sur Internet une manière de calculer l'aire d'un polygone à l'aide des coordonnées de ses sommets et j'ai trouvé cette solution.

> Pour la fonction sommets, je me suis dit que cette fonction augmenterait énormément la performance du jeu (à la place de garder en mémoire toutes 
les coordonnées de chaque point d'un segment, on peut juste garder en mémoire les coordonnées des sommets).

> Pour la fonction concatenation_safezone, on avait eu plusieurs idées, mais les idées précédant la fonction actuelle ne fonctionnaient pas toujours, et donc j'ai vu qu'à chaque fois que l'on capture une zone, soit :
- Le début et la fin de la zone capturée est entre 2 points de la safezone,
- Le début de la zone capturée est entre 2 points de la safezone mais la fin ne l'est pas et donc, tant que la fin n'est pas entre 2 points de la safezone, il faut les supprimer.
Les coordonnées de la safezone qui sont supprimées doivent être renversées car sinon, le polygone ne serait pas dans le bon ordre.

> La fonction debut_egal_fin n'est utile que pour les extrémités du polygone car, sans cette fonction, il faudrait rajouter, à chaque fonction utilisant l'index i+1 à la 
safezone, la condition qui vérifie si l'index == len((liste) - 1) ce qui doublerait la taille du code.

> Pour le déplacement des sparxs (non implémenté pour causes de problèmes techniques), nous utilisons les coordonnées des polygones qui composent la zone capturée. 
Lorsque le sparx se situe sur un point contenu dans une liste de polygones, la fonction va regarder quelle est le point situé avant ou après, en fonction du sens dans lequel 
tourne le sparx, et en fait sa destination. En comparant les valeurs des coordonnées actuelles et celles de la destination, le sparx pourra se diriger. 
Pour les mouvements internes : si un point se situe dans plusieurs listes différentes (donc différents polygones), les prochaines coordonnées sont ajoutés dans une liste, 
puis la destination finale est choisie de manière aléatoire.

> Pour le menu, on est allé pour un qui est simple pour ne pas trop ajouter trop de travail (avec les autres SAEs, TPs, etc). On s'est dit qu'il était possible de faire une 
fonction pour faire les boîtes avec du texte à l'intérieur mais il y aurait eu beaucoup de variables à mettre et on a décidé de juste copier coller le code (malgré la longueur des fonctions).

> Pour le Qix

========= Problèmes Rencontrés =========
- Certaines fonctions, comme debut_egal_fin ou concatenation_safezone, ne fonctionnent pas dans 100% des situations, et on n'arrive pas à trouver la source des problèmes. 
Ainsi, l'utilisation de ces fonctions peut entraîner des problèmes sur certains passages qui les utilisent (par exemple, pour les Sparx)

- Pour le mouvement des Sparx, notamment pour les raisons d'au-dessus

- Limite de temps : bien que le jeu semble simple, en théorie, à coder, certaines choses sont difficiles à implémenter dans les faits, et cela peut être une vraie source
de perte de temps. De plus, le temps pendant lequel on peut travailler sur le projet est très court, et cela est d'autant plus vrai en cette période de fin de semestre,
où s'entremêlent plein de projets, de soutenances, de partiels et de devoirs qui prennent, eux aussi, du temps. Les bugs que l'on découvre au fur et à mesure prennent 
également du temps à résoudre, et devoir ajouter toutes les variantes resserre encore le délai déjà initialement serré, résultant dans le fait que certaines choses 
soient manquantes, ou pas entièrement fonctionnelles.
