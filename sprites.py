import pygame


class Body(pygame.sprite.Sprite):
    def __init__(self,game,pos,size,color):
        self.game = game
        self.pos = pos
        self.size = size
        self.velocity = [0,0]
        self.display = pygame.Surface(self.size)
        self.display.fill(color) 

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1]).copy()

    def update(self, offset=[0,0]):
        self.apply_gravity()

    def apply_gravity(self):
        self.pos[1]+= 2

    def render(self,surf,offset = (0,0)):
        rect = self.rect()
        surf.blit(self.display, 
                  (rect[0] - offset[0], rect[1] - offset[1]))
        

class player(Body):
    def __init__(self, game, pos, size, color):
        super().__init__(game, pos, size, color)
        

    def update(self,movement):

        self.pos[0] += movement[0]
        self.pos[1] += movement[1] * 10
        
        super().update()

        
