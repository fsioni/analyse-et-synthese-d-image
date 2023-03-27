import sys
import cv2


def load_image(_img_path):
    _img = cv2.imread(_img_path)
    return _img


def resize_image(_img, _antialiasingSize):
    width = int(img.shape[1] / _antialiasingSize)
    height = int(img.shape[0] / _antialiasingSize)
    dim = (width, height)

    _img = cv2.resize(_img, dim, interpolation=cv2.INTER_AREA)
    return _img


def save_image(_img, _img_path):
    cv2.imwrite(_img_path, _img)


if __name__ == '__main__':
    # get the parameters
    if len(sys.argv) < 2:
        print('please input the parameters : image_path antialiasingSize')
        exit(1)

    img_path = sys.argv[1]
    img = load_image(sys.argv[1])

    antialiasingSize = int(sys.argv[2])
    img = resize_image(img, antialiasingSize)

    # ../images/output-before_resize.png should be ../images/output.png
    img_path = img_path.replace('before_resize', '')
    save_image(img, img_path + '_antialiasing_' + str(antialiasingSize) + '.jpg')
