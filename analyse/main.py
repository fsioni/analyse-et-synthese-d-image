import time
import cv2
import numpy as np
import sys
import os

debug = False
piece = -1

# Récupérer la couleur dominante dans une image
def couleur_dominante(_image):
    if (debug): print('Récupération de la couleur dominante...')
    pixels = np.float32(_image.reshape(-1, 3))

    # Paramètres de la fonction kmeans
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    # Liste des couleurs dominantes
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 1, flags)

    # On rend la liste avec d'unique couleur
    _, counts = np.unique(labels, return_counts=True)

    # On récupère la couleur dominante
    _dominant = palette[np.argmax(counts)]
    if (debug): print('Couleur dominante récupérée : ', _dominant)
    return _dominant


# récupérer la liste des pixels de couleur dominante dans une image avec une tolérance
def liste_pixel_dominants(image, couleur, tolerance):
    if (debug): print('Récupération de la liste des pixels de couleur dominante...')

    limite_base = couleur - tolerance
    limite_haut = couleur + tolerance

    masque = np.all((image >= limite_base) & (image <= limite_haut), axis=-1)

    indices = np.column_stack(np.nonzero(masque))


    if (debug): print('Liste des pixels de couleur dominante récupérée : ', len(indices))
    return indices


# remplacer si dans la liste par une couleur sinon par une autre
def remplacer_couleur(_image, _liste, border=False):
    if (debug): print('Création de l\'image noir/blanc...')
    # Si dans la liste, on met en blanc
    # Sinon on le met en noir
    # On crée une image à la même taille que l'image de base, mais en noir
    _image = np.zeros((_image.shape[0], _image.shape[1], 3), np.uint8)
    for pixel in _liste:
        _image[pixel[0]][pixel[1]] = [255, 255, 255]

    # On hardcode le contour en blanc de x pixels de large
    if border:
        x = border
        _image[0:x, 0:_image.shape[1]] = [255, 255, 255]
        _image[_image.shape[0] - x:_image.shape[0], 0:_image.shape[1]] = [255, 255, 255]
        _image[0:_image.shape[0], 0:x] = [255, 255, 255]
        _image[0:_image.shape[0], _image.shape[1] - x:_image.shape[1]] = [255, 255, 255]

    if (debug): print('Image créée')
    cv2.imwrite('image_NB.png', _image)


    # On supprime les petits amas de pixels noirs
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    _image = cv2.morphologyEx(_image, cv2.MORPH_OPEN, kernel)

    # On ferme les petits troue des pieces
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    _image = cv2.morphologyEx(_image, cv2.MORPH_CLOSE, kernel)
    return _image

# Trier les amas de pixels par colonne puis par ligne avec une tolérance de 10 pixels
def trier_amas(contours, tolerance=50):
    # Tri des contours par ordre croissant en fonction de leur position en Y, puis en X
    contours_sorted = sorted(
        contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0])
    )

    # Initialisation des lignes et de la première ligne avec le premier contour
    lines = []
    current_line = [contours_sorted[0]]
    current_line_y = cv2.boundingRect(contours_sorted[0])[1]

    # Parcours des contours triés et regroupement par ligne
    for contour in contours_sorted[1:]:
        y = cv2.boundingRect(contour)[1]
        if abs(y - current_line_y) <= tolerance:  # Si le contour est sur la même ligne
            current_line.append(contour)
        else:  # Si le contour est sur une nouvelle ligne
            lines.append(current_line)
            current_line = [contour]
            current_line_y = y

    # Ajout de la dernière ligne de contours
    lines.append(current_line)

    # Tri des contours à l'intérieur de chaque ligne par ordre croissant en fonction de leur position en X
    sorted_lines = [
        sorted(line, key=lambda c: cv2.boundingRect(c)[0]) for line in lines
    ]

    # Fusion des contours triés par ligne pour obtenir la liste finale des contours triés par lignes et colonnes
    sorted_contours = [contour for line in sorted_lines for contour in line]

    return sorted_contours


# Trouver les amas de pixels noir
def identification_amas(_image):
    if (debug): print('Identification des amas de pixels noirs...')
    # On récupère les contours de l'image
    contours, _ = cv2.findContours(_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # On récupère les contours des amas de pixels noirs
    contours_amas = []
    for contour in contours:
        # On vérifie que le contour fait au moins 50 pixels de large ([2] = largeur) et de haut ([3] = hauteur)
        if cv2.boundingRect(contour)[2] > 50 and cv2.boundingRect(contour)[3] > 50:
            contours_amas.append(contour)


    # on supprime le plus grand contour (le contour de l'image)
    contours_amas.pop(0)
    if (debug): print('Amas de pixels noirs identifiés : ', len(contours_amas))
    # Simplifier les contours
    contours_amas = [cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True) for contour in contours_amas]
    contours_amas = trier_amas(contours_amas)
    return contours_amas

def encadrer_amas(_image, _contours):
    if (debug):  print('Encadrement des amas de pixels noirs...')
    # on copie l'image de base
    _image = _image.copy()
    # On encadre les amas de pixels noirs
    for contour in _contours:
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On encadre le contour
        cv2.rectangle(_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if (debug): print('Amas de pixels noirs encadrés')
    return _image

def numeroter_amas(_image, _contours):
    if (debug): print('Numérotation des amas de pixels noirs...')
    # On encadre les amas de pixels noirs
    for i, contour in enumerate(_contours):
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On écrit le text en plein milieu du contour
        cv2.putText(_image, str(i + 1), (x + int(w / 2), y + int(h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if (debug): print('Amas de pixels noirs numérotés')
    return _image

class Piece:
    def __init__(self, x, y, w, h, top, bottom, left, right, index):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.sides = [top, bottom, left, right]
        self.index = index
        self.used = False

piecesTab = []

def piece_info(_contours, _index, image):
    if (debug):
        print("====================================")
        print('Pièce n°', _index)

    # On récupère les coordonnées du contour
    x, y, w, h = cv2.boundingRect(_contours[_index])
    piece = Piece(x, y, w, h, False, False, False, False, _index)
    # On affiche le contour
    image = cv2.drawContours(image, _contours, _index, (0, 255, 0), 2)

    # On fait une sous fonction pour éviter de répéter le code :)
    def scan_side(start, end, step, side):
        transitions = 0
        inside_contour = cv2.pointPolygonTest(_contours[_index], start, False) > 0
        # Si premier point dans le contour, on commence à 1
        # Sinon on commence à 0
        current = 1 if inside_contour else 0
        premierPts = False
        dernierPts = False
        derniereTransition = False
        for current in range(1, end):
            point = tuple(map(lambda x, y: x + y * current, start, step))
            current_inside_contour = cv2.pointPolygonTest(_contours[_index], point, False) > 0

            # Si on change de côté du contour
            # Mais que la dernière transition est pas trop proche
            if current_inside_contour != inside_contour and derniereTransition - current < 5:
                derniereTransition = current # On met à jour la dernière transition
                transitions += 1
                dernierPts = current
                cv2.circle(image, point, 1, (0, 0, 255), 2)

            inside_contour = current_inside_contour # On met à jour la valeur de inside_contour

            # Si on est dans le contour et qu'on a pas encore trouvé le premier point
            if (current_inside_contour and not premierPts):
                premierPts = current
                # On fait un point bleu sur le premier point
                cv2.circle(image, point, 1, (255, 0, 0), 2)

        distance = dernierPts - premierPts
        # Différence entre le premier et le dernier point
        if (transitions == 2 and distance > 60):
            transitions = 0

        sideShape = trouOrProt(transitions, x, y, w, h, side, image)
        piece.sides[side] = sideShape

    dist = 15 # la distance entre le bord et la ligne de scan
    # les infos suivant les côtés
    sides = [
        ((x, y + dist), (1, 0), w, "Haut"),
        ((x, y + h - dist), (1, 0), w, "Bas"),
        ((x + dist, y), (0, 1), h, "Gauche"),
        ((x + w - dist, y), (0, 1), h, "Droite")
    ]

    # On scanne les 4 côtés
    for i, (start, step, end, name) in enumerate(sides):
        if (debug): print(name, ":")
        scan_side(start, end, step, i)

    # On retourne la partie de l'image
    imagePiece = image[y:y + h, x:x + w]
    piecesTab.append(piece)
    return imagePiece


# Suivant le nombre d'intersections, on affiche un message différent et un symbole différent sur l'image
def trouOrProt(nbIntersec, x, y, w, h, side, image, dist=15):
    # on associe le nb d'intersections à un message et un symbole
    messages_and_formes = {
        0: ("C'est un bord.", "Bord"),
        2: ("Il y a une protubérance.", "Prot"),
        4: ("Il y a un trou.", "Trou")
    }

    # on récupère le message et le symbole associés (si on sais pas, on affiche "Forme inconnue.")
    message, forme = messages_and_formes.get(nbIntersec, ("Forme inconnue.", "?"))
    if (debug): print(message)

    # on récupère la taille du texte que l'on va afficher
    textSize = cv2.getTextSize(forme, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

    # on récupère les positions possibles du texte (suivant le côté)
    positions = [
        (x + int((w - textSize[0]) / 2), y + dist),
        (x + int((w - textSize[0]) / 2), y + h - dist),
        (x + dist - int(textSize[0] / 2), y + int(h / 2)),
        (x + w - dist - int(textSize[0] / 2), y + int(h / 2))
    ]

    # On met un rectangle autour du texte
    # cv2.rectangle(image, (positions[side][0] - 5, positions[side][1] + 5), (positions[side][0] + textSize[0] + 5, positions[side][1] - textSize[1] - 5), (255, 255, 255), 2)
    # on affiche le texte
    posX, posY = positions[side]
    cv2.putText(image, forme, (posX, posY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return forme

def endTime(start):
    # end time
    end = time.time()
    elapsed = round(end - start, 2)
    # total time taken
    print(f"Analyse terminée en {elapsed} secondes")

if __name__ == '__main__':
    # # On récupère le premier argument pour savoir si on affiche les détails ou pas
    # debug = len(sys.argv) > 1 and sys.argv[1] == "debug"

    # on récupère les arguments de la ligne de commande (si il y en a)
    args = sys.argv[1:]
    for arg in args:
        if arg == "debug":
            debug = True
        # Si un nombre on définit la pièce à analyser
        elif arg.isdigit():
            piece = int(arg)

    print("Début de l'analyse...")
    # start time
    start = time.time()
    # Open image.jpeg
    image = cv2.imread('image.jpeg')
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageBase = cv2.GaussianBlur(image, (5, 5), 0) # blur pour réduire le bruit
    cv2.imwrite('image_gris.png', imageGray)
    # Couleur dominante
    dominant = couleur_dominante(imageBase)
    # Afficher la couleur de fond

    # Récupérer la liste des pixels de couleur de fond
    liste = liste_pixel_dominants(imageBase, dominant, 23)

    # Remplacer la couleur de fond par du blanc
    imageNoirSurBlanc = remplacer_couleur(imageBase, liste, 10)

    # enregistrer l'image noir sur blanc
    cv2.imwrite('image_noir_sur_blanc.png', imageNoirSurBlanc)

    # image to CV_8UC1
    imageContours = cv2.cvtColor(imageNoirSurBlanc, cv2.COLOR_BGR2GRAY)
    # On récupère les amas de pixels noirs
    contourAmas = identification_amas(imageContours)

    # Encadrer les amas de pixels noirs
    imageContours = encadrer_amas(image, contourAmas)
    # Numéroter les amas de pixels noirs
    imageContours = numeroter_amas(imageContours, contourAmas)

    # Enregistrer l'image avec les amas de pixels noirs
    cv2.imwrite('image_contours.png', imageContours)

    # On le fait pour toutes les pièces
    # Dabord on regarde si le dossier pieces existe, si non on le crée
    if not os.path.exists('pieces'):
        os.makedirs('pieces')

    # On créee une fenêtre qui souvre en premier plan
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_TOPMOST, 1)

    # Si on a spécifié une pièce à analyser
    if (piece != -1 and piece < len(contourAmas)):
        imagePiece = piece_info(contourAmas, piece, image)
        endTime(start)
        cv2.imwrite('pieces/image_piece_' + str(piece) + '.png', imagePiece)
        # On affiche l'image
        cv2.imshow('image', imagePiece)
        cv2.waitKey(0)
    else: # Sinon on analyse toutes les pièces
        for i in range(0, len(contourAmas)):
            imagePiece = piece_info(contourAmas, i, image)
            cv2.imwrite('pieces/image_piece_' + str(i) + '.png', imagePiece)
        endTime(start)
        cv2.imwrite('image_final.png', image)

    # On ferme la fenêtre
    cv2.destroyAllWindows()

    def isOkay(_piece, _index, _col, _row):
        valide = True
        # Si sur la première ligne il faut que la pièce ait un bord en haut
        if (_index < _col):
            if (_piece.sides[0] != "Bord"):
                valide = False

        # Si sur la première colonne il faut que la pièce ait un bord à gauche
        if (_index % _col == 0):
            if (_piece.sides[2] != "Bord"):
                valide = False

        # Si sur la dernière ligne il faut que la pièce ait un bord en bas
        if (_index >= _col * (_row - 1)):
            if (_piece.sides[1] != "Bord"):
                valide = False

        # Si sur la dernière colonne il faut que la pièce ait un bord à droite
        if (_index % _col == _col - 1):
            if (_piece.sides[3] != "Bord"):
                valide = False

        return valide

    def getVoisins(_solution, _col, _row, _index):
        # On récupère les voisins
        voisins = [None, None, None, None]
        solutionLen = len(_solution)
        # On récupère le voisin du dessus
        if (_index >= _col and _index - _col < solutionLen):
            voisins[0] = _solution[_index - _col]
        # On récupère le voisin du dessous
        if (_index < _col * (_row - 1) and _index + _col < solutionLen):
            voisins[1] = _solution[_index + _col]
        # On récupère le voisin de gauche
        if (_index % _col != 0 and _index - 1 < solutionLen):
            voisins[2] = _solution[_index - 1]
        # On récupère le voisin de droite
        if (_index % _col != _col - 1 and _index + 1 < solutionLen):
            voisins[3] = _solution[_index + 1]

        return voisins

    debug = ""

    def isMatching(side1, side2):
        global debug
        # Si un des deux côtés est un bord on ne peut pas les emboiter
        if (side1 == "Bord" or side2 == "Bord"):
            debug += "Bord\n"
            return False
        # Si les deux côtés sont identiques on ne peut pas les emboiter
        if (side1 == side2):
            debug += "Identique\n"
            return False
        # Si les deux côtés sont inversés on peut les emboiter
        return True

    def oposedSide(_side):
        if (_side == 0):
            return 1
        elif (_side == 1):
            return 0
        elif (_side == 2):
            return 3
        elif (_side == 3):
            return 2
        return -1

    # Résoudre un puzzle de façon récursive de taille _col x _row
    def recursive_puzzle_solver(_piecesTab, _solution, _col, _row):
        global debug
        if (len(_solution) == _col * _row):
            return _solution
        # On récupère l'index de la pièce à trouver
        index = len(_solution)
        # on essaye de trouver une pièce qui correspond
        for i in range(0, len(_piecesTab)):
            debug += "Piece " + str(i) + " / " + str(len(_piecesTab)) + " pour la position " + str(index) + " / " + str(_col * _row) + "\n"

            # On regarde si la pièce est déjà dans la solution
            if (_piecesTab[i] in _solution):
                debug += "Déjà dans la solution - Nop\n"
                continue
            debug += "Pas déjà dans la solution - Ok\n"
            # On regarde si la pièces est valide pour la position
            if (not isOkay(_piecesTab[i], index, _col, _row)):
                debug += "Pas valide pour la position - Nop\n"
                continue
            debug += "Valide pour la position - Ok\n"
            # On récupère les pièces voisines
            voisins = getVoisins(_solution, _col, _row, index)
            # On regarde si les pièces voisines correspondent
            valide = True
            for j in range(0, len(voisins)):
                debug += "Voisin " + str(j) + " / " + str(len(voisins)) + " "
                if (voisins[j] == None):
                    debug += "Pas de voisin - Ok\n"
                    continue
                if (not isMatching(_piecesTab[i].sides[j], voisins[j].sides[oposedSide(j)])):
                    debug += "Pas valide pour les voisins - Nop at side "+str(j)+" (" + _piecesTab[i].sides[j] + ",  " + voisins[j].sides[oposedSide(j)] + ")\n"
                    valide = False
                    break

            # Si la pièce est valide on l'ajoute à la solution
            if (not valide):
                debug += "Pas valide pour les voisins - Nop\n"
                continue

            debug += "Valide pour les voisins - Ok\n"
            _solution.append(_piecesTab[i])
            # On essaye de résoudre le puzzle
            solution = recursive_puzzle_solver(_piecesTab, _solution, _col, _row)
            # Si on a trouvé une solution on la retourne
            if (solution != None):
                return solution
            # Sinon on retire la pièce de la solution
            _solution.pop()


        # Si on a pas trouvé de solution on retourne None
        return None

    # On essaye de résoudre le puzzle
    Col = 7
    Row = 4
    solution = recursive_puzzle_solver(piecesTab, [], Col, Row)

    # Si on a trouvé une solution on l'affiche
    imageRecomposer = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
    posX = 0
    posY = 0
    pieceHeight = image.shape[0] // Row
    pieceWidth = image.shape[1] // Col
    if (solution != None):
        print("Solution trouvée")
        # On recrée l'image
        for y in range(0, Row):
            posX = 0
            for x in range(0, Col):
                piece = solution[y * Col + x]
                # On fait une position centrée
                posXcenter = posX + (pieceWidth - piece.w) // 2
                posYcenter = posY + (pieceHeight - piece.h) // 2
                print(solution[y * Col + x].sides, end=" ")
                imagePiece = image[piece.y:piece.y + piece.h, piece.x:piece.x + piece.w]
                imageRecomposer[posYcenter:posYcenter + piece.h, posXcenter:posXcenter + piece.w] = imagePiece
                posX += pieceWidth
            print()
            posY += pieceHeight
        cv2.imwrite("resultat.png", imageRecomposer)
    else:
        print("Pas de solution trouvée")

    # 2crire le résultat dans un fichier en le vidant avant
    f = open("resultat.txt", "w")
    f.write(debug)
    f.close()





