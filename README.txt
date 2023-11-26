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




========= Problèmes Rencontrés =========
- Certaines fonctions, comme debut_egal_fin ou concatenation_safezone, ne fonctionnent pas dans 100% des situations, et on n'arrive pas à trouver la source des problèmes. 
Ainsi, l'utilisation de ces fonctions peut entraîner des problèmes sur certains passages qui les utilises (par exemple, pour les Sparx)
- Pour le mouvement des Sparx, notamment pour les raisons d'au-dessus
- Limite de temps : bien que le jeu semble simple, en théorie, à coder, certaines choses sont difficiles à implémenter dans les faits, et cela peut être une vrai source
de perte de temps.
[Romain : Cela est d'autant plus vrai pour moi, qui suis moins à l'aise sur Python que Jérémy. J'ai dû passer plus de 60H pour avoir un Sparx qui fonctionne correctement, et encore, seul l'un des deux fonctionne bien ...
C'est ce genre de choses, qui sont normalement simple à faire mais avec lesquelles j'ai du mal, qui me donnent une réel sensation de n'être qu'un poids mort pour mon binôme]
