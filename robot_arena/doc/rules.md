# Rules

## Requirements
Pour mettre en place les règles
- il faut une authorité (un juge) qui puisse vérifier la bonne utilisation.

Pour mettre en place les bonus/malus
- il faut au préalable complexifier le code pour ajouter des obstacles (murs, trous, etc..)

## Arena
Ce sont les règles qui peuvent s'appliquer uneiquement à une arène.

Exemple :
- La  cible reste cachée aux robots, seule l'authorité (et l'arène) connaissent la position

## Robots
Ce sont les règles qui ne s'appliquent qu'aux robots.

Exemple :
- interdiction de faire marche arrière
- interdiction de faire des déplacements en diagonale
etc...

## Bonus/Malus
C'est une règle spécifique qui peut s'apppliquer (pour l'instant) que sur les robots.
C'est un peu une carte chance (ou pas).

Exemple :
- bonus : possibilité de traverser les obstacles
- bonus : une "vision" des voisins plus grande
- malus : une perte de rapidité
    - au lieu de parcourir une case en 1 tour, il en faut 2
- malus : aucune vision des cases voisines

## Définition (code)
il faut : 
- un nom
- une description
- des valeurs (bool ou int)

### pour l'arène
liste des valeurs possibles imaginées :

- show_goal (True/False)
- show_opponent (True/False)

### pour les robots
liste des valeurs possibles imaginées :

- can_move_backward (True/False)
- pull_down_speed (0..100) Facteur
- pull_up_speed (0..100) Facteur