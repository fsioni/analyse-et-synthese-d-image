import cv2
import numpy as np


# Récupérer la couleur dominante dans une image
def couleurDominante(image):
    print('Récupération de la couleur dominante...')
    pixels = np.float32(image.reshape(-1, 3))

    # Paramètres de la fonction kmeans
    n_colors = 5
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    # Liste des couleurs dominantes
    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 1, flags)

    # On rend la liste avec d'unique couleur
    _, counts = np.unique(labels, return_counts=True)

    # On récupère la couleur dominante
    dominant = palette[np.argmax(counts)]
    return dominant


# récupérer la liste des pixels de couleur dominante dans une image avec une tolérance
def listePixelDominants(image, couleur, tolerance, gris=False):
    print('Récupération de la liste des pixels de couleur dominante...')
    liste = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixelColor = image[i][j]
            limiteBase = couleur - tolerance
            limiteHaut = couleur + tolerance
            condHaut = pixelColor[0] <= limiteHaut[0] and pixelColor[1] <= limiteHaut[1] and pixelColor[2] <= \
                       limiteHaut[2]
            condBase = pixelColor[0] >= limiteBase[0] and pixelColor[1] >= limiteBase[1] and pixelColor[2] >= \
                       limiteBase[2]
            if condHaut and condBase:
                liste.append([i, j])
    return liste


# remplacer si dans la liste par une couleur sinon par une autre
def remplacerCouleur(image, liste):
    print('Image noir et blanc...')
    # Si dans la liste on met en blanc
    # Sinon on le met en noir
    # On crée une image a la même taille que l'image de base mais en noir
    image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
    for pixel in liste:
        image[pixel[0]][pixel[1]] = [255, 255, 255]

    # On hardcode le contour en blanc de 5 pixels de large
    image[0:5, 0:image.shape[1]] = [255, 255, 255]
    image[image.shape[0] - 5:image.shape[0], 0:image.shape[1]] = [255, 255, 255]
    image[0:image.shape[0], 0:5] = [255, 255, 255]
    image[0:image.shape[0], image.shape[1] - 5:image.shape[1]] = [255, 255, 255]

    print('Image créée')
    return image


# Trouver les amas de pixels noir
def identificationAmas(image):
    print('Identification des amas de pixels noirs...')
    # On récupère les contours de l'image
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # On récupère les contours des amas de pixels noirs
    contoursAmas = []
    for contour in contours:
        # On récupère les coordonnées du contour
        x, y, w, h = cv2.boundingRect(contour)
        # On vérifie que le contour fait au moins 100 pixels de large
        if w > 100:
            contoursAmas.append(contour)
    return contoursAmas


if __name__ == '__main__':
    # Open image.jpeg
    imageBase = cv2.imread('image.jpeg')
    imageGray = cv2.cvtColor(imageBase, cv2.COLOR_BGR2GRAY)
    # Flou gaussien pour lisser l'image
    imageBase = cv2.GaussianBlur(imageBase, (5, 5), 0)
    dominant = couleurDominante(imageBase)
    # Afficher la couleur de fond
    print('La couleur du fond est :', dominant)

    # Récupérer la liste des pixels de couleur de fond
    liste = listePixelDominants(imageBase, dominant, 25)
    print('Nombre de pixels de couleur de fond :', len(liste))

    # Remplacer la couleur de fond par du blanc
    image = remplacerCouleur(imageBase, liste)

    # image to CV_8UC1
    imageAma = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contourAmas = identificationAmas(imageAma)
    print('Nombre d\'amas de pixels noirs :', len(contourAmas))

    # Afficher les amas de pixels noirs
    cv2.drawContours(image, contourAmas, -1, (0, 255, 0), 3)

    # Créer la fenêtre d'affichage de l'image en premier plan
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)

    # Afficher l'image
    cv2.imshow('image', image)

    # Boucle infinie pour afficher l'image
    while True:
        key = cv2.waitKey(30) & 0x0FF
        if key == 27 or key == ord('q'):
            print('arrêt du programme par l\'utilisateur')
            break

    cv2.destroyWindow('image')
    print('Fin du programme')
