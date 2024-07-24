import pygame
import os
from pygame.time import get_ticks

PATH_IMG = 'img/'
def load_img(path):
    img = pygame.image.load(PATH_IMG + path).convert()
    return img

def load_imgs(path):
    imgs = []

    for i in os.listdir(PATH_IMG + path):
        imgs.append(load_img(path + '/' + i))
    
    return imgs


class Timer:
    def __init__(self,duration):
        self.duration = duration
        self.start = 0
        self.active = False
        

    def activate(self):
        self.active = True
        self.start = get_ticks()

    def deativate(self):
        self.active= False
        self.start = 0
        print("sus")
    def update(self):
        if self.active:
            current_time = get_ticks()
            print(self.start)
            print(self.duration)
            if  current_time <= self.duration:
                print('sus')
                self.deativate()
         