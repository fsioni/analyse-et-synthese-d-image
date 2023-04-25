### TP noté - Analyse d'images 2022/2023
Par :
- Ballouard Julien p2006861
- Sioni Fares p1907037

## Dépendances :
- cv2
- numpy

## Fonctionnement :
Pour lancer le programe, il suffit de lancer le fichier `main.py` avec Python3.
- `python3 main.py`

Il est possible d'ajouter des argument tels que :
- `python3 main.py image.jpeg` pour choisir l'image à analyser (par défaut, l'image est `puzzle.jpeg`)
- `python3 main.py debug` pour afficher plus d'informations sur le déroulement du programme dans la console
- `python3 main.py {numbre}` pour afficher précisément une pièce du puzzle
Tout ces arguments peuvent être combinés, sans ordre particulier.

## Bonus implémentés :
- Extraire les pieces du puzzle (dans le dossier `pieces/`)
- Identifier et extraire les contours des pièces du puzzle
- Décrire la forme des pièces du puzzle (Bord/Trou/Protubérance)

## Fichiers de sortie :
- `puzzle_contours.png` -> image de base avec les pièces du puzzle encadrées par des rectangles et identifiées par un numéro
- `puzzle_global.png` -> image de base avec les pièces, leur contours et les infos sur leur côté (Bord/Trou/Protubérance)
- `puzzle_gris.png` -> image de base en niveau de gris
- `puzzle_NB.png` -> image de base en noir et blanc
- `puzzle_NBNett.png` -> image de base en noir et blanc (améliorée)
- `puzzle_resolue.png` -> image du puzzle résolu (ne prend pas en compte les couleurs et les rotations par manque de temps)

## Dérouler du processus :
- Lecture de l'image
- Mise de l'image en nuance de gris
- Ajout d'un flou gaussien pour diminuer le bruit
- Récupération de la couleur dominante de l'image (le fond)
- Récupération des pixels qui sont proche de cette couleur (le fond)
- On remplace ces pixels par du blanc et les autres par du noir sur une nouvelle image pour obtenir `puzzle_NBNett.png`
- On identifie les différents contours de l'image (les pièces du puzzle)
- On les encadre et les numérote pour obtenir `puzzle_contours.png`
- Pour chaques pièces, on scan chaques côté à 15 pixels du bord pour déterminer la forme de la pièce (Bord/Trou/Protubérance) en comptant le nombre de fois que l'ont entre dans le contour de la pièce
- Et on affiche les débug sur l'image directement pour obtenir `pieces/puzzle_piece_{num}.png`
- Puis on enregistre l'image avec les infos sur les pièces pour obtenir `puzzle_global.png`

# Solver :
- On utilise l'objet piece pour stocker les informations sur les pièces
- On essaye une pièce place 1 puis une pièce place 2 si c'est bon on continue sinon on redescend jusqu'à trouver une pièce qui colle et on continue pour trouver la solution.
