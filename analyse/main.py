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
def liste_pixel_dominants(_image, couleur, tolerance, gris=False):
    print('Récupération de la liste des pixels de couleur dominante...')
    _liste = []
    for i in range(_image.shape[0]):
        for j in range(_image.shape[1]):
            pixel_color = _image[i][j]
            limite_base = couleur - tolerance
            limite_haut = couleur + tolerance
            cond_haut = pixel_color[0] <= limite_haut[0] and pixel_color[1] <= limite_haut[1] and pixel_color[2] <= \
                        limite_haut[2]
            cond_base = pixel_color[0] >= limite_base[0] and pixel_color[1] >= limite_base[1] and pixel_color[2] >= \
                        limite_base[2]
            if cond_haut and cond_base:
                _liste.append([i, j])
    return _liste


# remplacer si dans la liste par une couleur sinon par une autre
def remplacer_couleur(_image, _liste):
    print('Image noir et blanc...')
    # Si dans la liste, on met en blanc
    # Sinon on le met en noir
    # On crée une image à la même taille que l'image de base, mais en noir
    _image = np.zeros((_image.shape[0], _image.shape[1], 3), np.uint8)
    for pixel in _liste:
        _image[pixel[0]][pixel[1]] = [255, 255, 255]

    # On hardcode le contour en blanc de x pixels de large
    x = 6
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
    return contours_amas


if __name__ == '__main__':
    # start time
    start = time.time()

    # Open image.jpeg
    imageBase = cv2.imread('image.jpeg')
    imageGray = cv2.cvtColor(imageBase, cv2.COLOR_BGR2GRAY)
    # Flou gaussien pour lisser l'image
    imageBase = cv2.GaussianBlur(imageBase, (5, 5), 0)
    dominant = couleur_dominante(imageBase)
    # Afficher la couleur de fond
    print('La couleur du fond est :', dominant)

    # Récupérer la liste des pixels de couleur de fond
    liste = liste_pixel_dominants(imageBase, dominant, 25)
    print('Nombre de pixels de couleur de fond :', len(liste))

    # Remplacer la couleur de fond par du blanc
    image = remplacer_couleur(imageBase, liste)

    # image to CV_8UC1
    imageAma = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contourAmas = identification_amas(imageAma)
    print('Nombre d\'amas de pixels noirs :', len(contourAmas))

    # Afficher les amas de pixels noirs
    cv2.drawContours(image, contourAmas, -1, (0, 255, 0), 3)

    # Créer la fenêtre d'affichage de l'image en premier plan
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

    # Afficher l'image
    cv2.imshow('image', image)

    # enregistrer l'image
    cv2.imwrite('image.png', image)

    # end time
    end = time.time()
    elapsed = round(end - start, 2)
    print('Temps d\'exécution :', elapsed, ' secondes')

    # Boucle infinie pour afficher l'image
    while True:
        key = cv2.waitKey(30) & 0x0FF
        if key == 27 or key == ord('q'):
            print('arrêt du programme par l\'utilisateur')
            break

    cv2.destroyWindow('image')
    print('Fin du programme')
