import pygame
import os

PATH_IMG = 'img/'
def load_img(path):
    img = pygame.image.load(PATH_IMG + path).convert()
    return img

def load_imgs(path):
    imgs = []

    for i in os.listdir(PATH_IMG + path):
        imgs.append(load_img(path + '/' + i))
    
    return imgs 