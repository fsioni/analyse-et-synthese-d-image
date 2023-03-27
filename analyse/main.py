import cv2
import numpy as np

# Open image.jpeg
image = cv2.imread('image.jpeg')
imageGris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('img', imageGris)

while True:
    key = cv2.waitKey(30) & 0x0FF
    if key == 27 or key == ord('q'):
        print('arrêt du programme par l\'utilisateur')
        break

cv2.destroyWindow('img')