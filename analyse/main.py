import time

import cv2
import numpy as np

# Récupérer la couleur dominante dans une image
def couleur_dominante(_image):
    print('Récupération de la couleur dominante...')
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
    return _dominant


# récupérer la liste des pixels de couleur dominante dans une image avec une tolérance
def liste_pixel_dominants(image, couleur, tolerance):
    print('Récupération de la liste des pixels de couleur dominante...')

    limite_base = couleur - tolerance
    limite_haut = couleur + tolerance

    masque = np.all((image >= limite_base) & (image <= limite_haut), axis=-1)

    indices = np.column_stack(np.nonzero(masque))

    return indices


# remplacer si dans la liste par une couleur sinon par une autre
def remplacer_couleur(_image, _liste, border=False):
    print('Image noir et blanc...')
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

    print('Image créée')
    return _image


# Trouver les amas de pixels noir
def identification_amas(_image):
    print('Identification des amas de pixels noirs...')
    # On récupère les contours de l'image
    contours, hierarchy = cv2.findContours(_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # On récupère les contours des amas de pixels noirs
    contours_amas = []
    for contour in contours:
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On vérifie que le contour fait au moins 100 pixels de large
        if w > 100:
            contours_amas.append(contour)


    # on supprime le plus grand contour (le contour de l'image)
    contours_amas.pop(0)
    return contours_amas

def encadrer_amas(_image, _contours):
    print('Encadrement des amas de pixels noirs...')
    # on copie l'image de base
    _image = _image.copy()
    # On encadre les amas de pixels noirs
    for contour in _contours:
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On encadre le contour
        cv2.rectangle(_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return _image

def numeroter_amas(_image, _contours):
    print('Numérotation des amas de pixels noirs...')
    # On encadre les amas de pixels noirs
    for i, contour in enumerate(_contours):
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On écrit le text en plein milieu du contour
        cv2.putText(_image, str(i + 1), (x + int(w / 2), y + int(h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return _image

# on fait une image qui contient une seul piece (amas de pixels noirs)
def piece_info(_contours, _index, image):
    # On récupère les coordonnées du contour
    x, y, w, h = cv2.boundingRect(_contours[_index])
    # On affiche le contour
    image = image.copy()
    image = cv2.drawContours(image, _contours, _index, (0, 255, 0), 2)
    # On compte le nombre de fois on traverse les verts sur le bord supérieur
    count = 0
    inGreen = False
    greenPos = []
    ptsUn = int(w/3)
    ptsDeux = int(w/3*2)
    for i in range(ptsUn, ptsDeux):
        vert = image[y + 10][x + i][1] == 255 and image[y + 10][x + i][0] == 0 and image[y + 10][x + i][2] == 0
        if vert:
            inGreen = True
            greenPos.append(i)
            if (inGreen) and (image[y + 10][x + i + 1][1] != 255):
                count += 1
                inGreen = False
                # On fait un point de rayon 5 au centre des greenPos
                # On trouve le point du milieu
                if len(greenPos) > 1:
                    greenPos = int((greenPos[0] + greenPos[-1]) / 2)
                else:
                    greenPos = greenPos[0]

                # On fait un point de rayon 5 au centre des greenPos
                cv2.circle(image, (x + greenPos, y + 10), 3, (0, 0, 255), -1)
                greenPos = []

    print('Nombre de fois on traverse verts sur le bord supérieur :', count)


    # On affiche juste l'image pour visualiser
    imagePiece = image[y:y + h, x:x + w]
    return imagePiece


if __name__ == '__main__':
    # start time
    start = time.time()

    # Open image.jpeg
    imageBase = cv2.imread('image.jpeg')
    imageGray = cv2.cvtColor(imageBase, cv2.COLOR_BGR2GRAY)
    imageBase = cv2.GaussianBlur(imageBase, (5, 5), 0) # blur pour réduire le bruit
    # Couleur dominante
    dominant = couleur_dominante(imageBase)
    # Afficher la couleur de fond
    print('La couleur du fond est :', dominant)

    # Récupérer la liste des pixels de couleur de fond
    liste = liste_pixel_dominants(imageBase, dominant, 25)
    print('Nombre de pixels de couleur de fond :', len(liste))

    # Remplacer la couleur de fond par du blanc
    imageNoirSurBlanc = remplacer_couleur(imageBase, liste, 10)

    # image to CV_8UC1
    imageContours = cv2.cvtColor(imageNoirSurBlanc, cv2.COLOR_BGR2GRAY)
    # On récupère les amas de pixels noirs
    contourAmas = identification_amas(imageContours)
    print('Nombre d\'amas de pixels noirs :', len(contourAmas))

    # Encadrer les amas de pixels noirs
    imageContours = encadrer_amas(imageBase, contourAmas)
    # Numéroter les amas de pixels noirs
    imageContours = numeroter_amas(imageContours, contourAmas)

    # enregistrer l'image noir sur blanc
    cv2.imwrite('image_noir_sur_blanc.png', imageNoirSurBlanc)

    # Enregistrer l'image avec les amas de pixels noirs
    cv2.imwrite('image_contours.png', imageContours)

    # On récupère l'image de la pièce 1
    imagePiece = piece_info(contourAmas, 0, imageBase)
    # Enregistrer l'image de la pièce 1
    cv2.imwrite('image_piece_1.png', imagePiece)

    # end time
    end = time.time()
    elapsed = round(end - start, 2)
    print('Temps d\'exécution :', elapsed, ' secondes')