import pygame
import sys
import time

from sprites import player
from utils import load_img,load_imgs
from tilemap import Tilemap


WIN_WIDTH = 640
WIND_HEIGHT = 480

COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
BLINK_LIGHT_EVENT = pygame.USEREVENT + 2
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
        self.assets = {'tiles/ground/ground': load_imgs('tiles/ground'),
                       'tiles/light/light': load_imgs('tiles/light')}
        self.tilemap = Tilemap(self, 32)
        self.scene = []
        self.blink_lights()
        self.load_level()
        
        self.scroll = [0, 0]
        self.keep = True
        

    def load_level(self):
        self.tilemap.load('map.json')

        for ground in self.tilemap.extract([('tiles/ground/ground',0)], keep = True):
            self.scene.append(pygame.Rect(4 + ground['pos'][0], 4 + ground['pos'][1], 32, 32))

    
        for light in self.tilemap.extract([('tiles/light/light',0)], keep = True):
            self.scene.append(pygame.Rect(4 + light['pos'][0], 4 + light['pos'][1], 32, 32))
    
        


    def blink_lights(self):
        
        pygame.time.set_timer(BLINK_LIGHT_EVENT, 5000)
        
        
        





    def run(self):
        pygame.time.set_timer(BLINK_LIGHT_EVENT, 5000)

        while self.running:
            
            self.display.fill((255,255,255))
            self.tilemap.render(self.display, self.scroll)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0] )/ 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1] )/ 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    sys.exit()
                if event.type == COYOTE_JUMP_EVENT:
                    print('aaaaa')
                    
                    self.player.was_on_floor = False
                    self.player.jumps-=1
                    pygame.time.set_timer(COYOTE_JUMP_EVENT, 0)
                
                if event.type == BLINK_LIGHT_EVENT:
                    
                    self.tilemap.visible_light()
                    
                    
             

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.movement[0] = True
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1)

                    if event.key == pygame.K_a:
                        self.movement[1] = True
                        self.player.velocity[0] = min(5, self.player.velocity[0] + 1) * -1

                    if event.key == pygame.K_w :
                        self.player.jump()
                   


                

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        self.movement[0]= False
                        self.player.velocity[0] = 0

                    if event.key == pygame.K_a:
                        self.movement[1] = False
                        self.player.velocity[0] = 0

                    if event.key == pygame.K_w:
                        self.movement[3] = False

          

             

            

            self.player.update( self.tilemap,
                [self.movement[0] - self.movement[1], self.movement[2]  -   self.movement[3] ]
            )
            
            self.player.render(self.display, render_scroll)

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)





g = Game()

while g.running:
    g.run()

pygame.quit()
sys.exit()
