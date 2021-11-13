# Robot Arena
## Règle de base
Le but de chaque robot est de se positionner sur la cible le plus rapidement possible.

algorithme de base : 
On calcul la distance entre la cible et le robot

```
distance = position_robot - position_cible
```

En fonction de la distance en X et Y, on avance de 1 dans la position souhaité ( X || Y || XY)


## Install & requirements

### Requirement 
- python 3.x

### Install 
```
pip install -r requirements.txt
```

## Run
```
python run.py
```
## Correspondance chiffre
99 - Cible

1-xx - Identifiant robot

## streamlit 
```
streamlit run ihm.py
```
## docker
buid 
```
docker build -t robot_streamlit:latest .
```
run 
```
docker run -it -p 35000:8501 robot_streamlit:latest
```

## Todo
- Mise en place de règle(s) d'arène
- Mise en place de règle pour chaque robot
    - contraintes de déplacement
- Modifier l'environnement 
    - ajouter des obstacles (mur, trou etc...)
- Cacher la cible aux robots
    - changer les règles du jeu (cf: Mise en place de règle(s) d'arène)

## Todo streamlit
- cache speed up formating