import pygame
import sys
import time

from sprites import player
from utils import load_img,load_imgs
from tilemap import Tilemap


WIN_WIDTH = 640
WIND_HEIGHT = 480

COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('shadow')


        self.screen = pygame.display.set_mode((WIN_WIDTH,WIND_HEIGHT))
        self.display = pygame.surface.Surface(((WIN_WIDTH//2,WIND_HEIGHT//2)))
        self.running = True
        self.clock = pygame.time.Clock()
        self.movement = [0,0,0,0]
        self.player = player(self,[12, 9],[32,32],(0,0,0))
        self.assets = {'tiles/ground/ground': load_imgs('tiles/ground')}
        self.tilemap = Tilemap(self, 32)
        self.scene = []
        self.load_level()
        self.isJump = False

    def load_level(self):
        self.tilemap.load('map.json')

        for ground in self.tilemap.extract([('tiles/ground/ground',0)], keep = True):
            self.scene.append(pygame.Rect(4 + ground['pos'][0], 4 + ground['pos'][1], 32, 32))




    def run(self):

        while self.running:
   
            self.display.fill((255,255,255))
            self.tilemap.render(self.display, offset = (0,0))
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()

             

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True

                    if event.key == pygame.K_a:
                        self.movement[1] = True

                    if event.key == pygame.K_w and not self.isJump:
                        self.player.velocity[1] = -3
                   


                

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0]= False

                    if event.key == pygame.K_a:
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[3] = False

                if keys[pygame.K_w]:
                    self.isJump = True

             

   

            self.player.update( self.tilemap,
                [self.movement[0] - self.movement[1], self.movement[2]  -   self.movement[3] ]
            )
            
            self.player.render(self.display,[0,0])

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)





g = Game()

while g.running:
    g.run()

pygame.quit()
sys.exit()
