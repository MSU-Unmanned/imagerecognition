# Made with reference to https://www.tutorialspoint.com/python_pillow/python_pillow_imagedraw_module.htm#:~:text=Drawing%20Shapes%20using%20%E2%80%98ImageDraw%E2%80%99%20module%201%20Line%20Following,Output%207%20Rectangle%20...%208%20Output%20More%20items

from PIL import *
from PIL import Image, ImageDraw, ImagePath, ImageFont
import cv2
import numpy as np
import math
import os


def downscale(img, size=(256, 256)):
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def rotate(img):
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)


def add_noise(img, noise_scale=1):
    # https://stackoverflow.com/questions/65303392/how-to-convert-python-np-array-to-cv2-image
    return cv2.add(img, (noise_scale*np.random.randn(*img.shape)).astype(type(img[0, 0, 0])))


def generate_polygon(sides, text='', face_color=(255, 50, 50), bg_color=(255, 255, 255), text_color=(255, 255, 255), font=ImageFont.FreeTypeFont(font='hussar-font.otf', size=132)):
    # Modified from https://www.geeksforgeeks.org/python-pil-imagedraw-draw-polygon-method/
    img = Image.new('RGB', (500, 500), bg_color)
    draw = ImageDraw.Draw(img)

    draw.regular_polygon(((250, 250), 200), sides,
                         fill=face_color, outline=face_color)
    draw.text((250-font.size/2, 250-font.size/2),
              text, fill=text_color, font=font)
    return img

# img=downscale(cv2.imread('test_data\\A_0.jpg'))
# cv2.imshow('original',img)
# cv2.imshow('noised',add_noise(img,0.5))


def generate_polygons(n_sides=(3, 4, 5, 6), colors=[(255, 0, 0), (0, 0, 255), (0, 255, 0)], texts=['A', 'B', 'C'], noise_scales=[0, 0.1, 0.2, 0.3, 0.4,1], n_rotates=3):
    # SUGGEST: Could perhaps be made more efficient
    polygons = []

    for n_side in n_sides:
        for color in colors:
            for text in texts:
                if not os.path.isdir('generated_images'):
                    os.mkdir('generated_images')

                for n_rotation in range(n_rotates+1):
                    polygon = generate_polygon(n_side, text, face_color=color)
                    polygon.save('interchange.png')
                    polygon = cv2.imread('interchange.png')

                    for i in range(n_rotation):
                        polygon = rotate(polygon)

                    for noise in noise_scales:
                        polygon = add_noise(polygon, noise_scale=noise)

                        save_string = os.path.join(
                            'generated_images', f'{n_side}gon_{text}_{color}color_{noise}noise_{n_rotation}rotates.png')
                        cv2.imwrite(save_string, polygon)
                        polygons.append(polygon)
    return polygons


if __name__ == "__main__":
    COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (0, 255, 255), (255, 0, 255), (255, 255, 255)]
    generate_polygons()

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
