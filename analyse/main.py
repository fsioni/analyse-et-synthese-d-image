import time
import cv2
import numpy as np
import sys
import os
debug = False

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
    return _image


# Trouver les amas de pixels noir
def identification_amas(_image):
    if (debug): print('Identification des amas de pixels noirs...')
    # On récupère les contours de l'image
    contours, _ = cv2.findContours(_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # On récupère les contours des amas de pixels noirs
    contours_amas = []
    for contour in contours:
        # On vérifie que le contour fait au moins 100 pixels de large ([2] = largeur)
        if cv2.boundingRect(contour)[2] > 100:
            contours_amas.append(contour)


    # on supprime le plus grand contour (le contour de l'image)
    contours_amas.pop(0)
    if (debug): print('Amas de pixels noirs identifiés : ', len(contours_amas))
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

def piece_info(_contours, _index, image):
    if (debug):
        print("====================================")
        print('Pièce n°', _index)

    # On récupère les coordonnées du contour
    x, y, w, h = cv2.boundingRect(_contours[_index])
    # On affiche le contour
    image = cv2.drawContours(image, _contours, _index, (0, 255, 0), 2)

    # On fait une sous fonction pour éviter de répéter le code :)
    def scan_side(start, end, step, dist, side):
        transitions = 0
        inside_contour = cv2.pointPolygonTest(_contours[_index], start, False) > 0

        for current in range(1, end):
            point = tuple(map(lambda x, y: x + y * current, start, step))
            current_inside_contour = cv2.pointPolygonTest(_contours[_index], point, False) > 0
            if current_inside_contour != inside_contour:
                transitions += 1
                cv2.circle(image, point, 1, (0, 0, 255), 2)
            inside_contour = current_inside_contour

        trouOrProt(transitions, x, y, w, h, side, image)

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
        scan_side(start, end, step, dist, i)

    # On retourne la partie de l'image
    imagePiece = image[y:y + h, x:x + w]
    return imagePiece


# Suivant le nombre d'intersections, on affiche un message différent et un symbole différent sur l'image
def trouOrProt(nbIntersec, x, y, w, h, side, image, dist=15):
    # on associe le nb d'intersections à un message et un symbole
    messages_and_formes = {
        4: ("Il y a un trou.", "T"),
        2: ("Il y a une protubérance.", "P")
    }

    # on récupère le message et le symbole associés (si on sais pas, on affiche "Forme inconnue.")
    message, forme = messages_and_formes.get(nbIntersec, ("Forme inconnue.", "IDK"))
    if (debug): print(message)

    # on récupère la taille du texte que l'on va afficher
    textSize = cv2.getTextSize(forme, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

    # on récupère les positions possibles du texte (suivant le côté)
    positions = [
        (x + int((w - textSize[0]) / 2), y + dist),
        (x + int((w - textSize[0]) / 2), y + h - dist),
        (x + dist + 10, y + int((h - textSize[1]) / 2)),
        (x + w - dist - 10, y + int((h - textSize[1]) / 2))
    ]

    # on affiche le texte
    posX, posY = positions[side]
    cv2.putText(image, forme, (posX, posY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


if __name__ == '__main__':
    # On récupère le premier argument pour savoir si on affiche les détails ou pas
    debug = len(sys.argv) > 1 and sys.argv[1] == "debug"
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
    liste = liste_pixel_dominants(imageBase, dominant, 25)

    # Remplacer la couleur de fond par du blanc
    imageNoirSurBlanc = remplacer_couleur(imageBase, liste, 10)

    # image to CV_8UC1
    imageContours = cv2.cvtColor(imageNoirSurBlanc, cv2.COLOR_BGR2GRAY)
    # On récupère les amas de pixels noirs
    contourAmas = identification_amas(imageContours)

    # Encadrer les amas de pixels noirs
    imageContours = encadrer_amas(image, contourAmas)
    # Numéroter les amas de pixels noirs
    imageContours = numeroter_amas(imageContours, contourAmas)

    # enregistrer l'image noir sur blanc
    cv2.imwrite('image_noir_sur_blanc.png', imageNoirSurBlanc)

    # Enregistrer l'image avec les amas de pixels noirs
    cv2.imwrite('image_contours.png', imageContours)

    # On le fait pour toutes les pièces
    # Dabord on regarde si le dossier pieces existe, si non on le crée
    if not os.path.exists('pieces'):
        os.makedirs('pieces')
    for i in range(0, len(contourAmas)):
        imagePiece = piece_info(contourAmas, i, image)
        cv2.imwrite('pieces/image_piece_' + str(i) + '.png', imagePiece)

    cv2.imwrite('image_final.png', image)

    # end time
    end = time.time()
    elapsed = round(end - start, 2)
    print('Fin de l\'analyse ! (', elapsed, ' secondes)')