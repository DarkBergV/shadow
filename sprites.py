from shutil import move
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
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self,tilemap,movement, offset=[0,0]):
        self.apply_gravity()
        framemove = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        
        self.pos[0] += framemove[0]
        
        

                

        self.pos[1] += framemove[1]
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            print(rect)
            if body_rect.colliderect(rect):
                
                if framemove[1] > 0:
                    body_rect.bottom = rect.top
                if framemove[1] < 0:
                    body_rect.top = rect.bottom

                self.pos[1] = body_rect.y
        
        


    def apply_gravity(self):
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

    def render(self,surf,offset = (0,0)):
        rect = self.rect()
        surf.blit(self.display, 
                  (rect[0] - offset[0], rect[1] - offset[1]))
        

class player(Body):
    def __init__(self, game, pos, size, color):
        super().__init__(game, pos, size, color)
        

    def update(self,tilemap, movement):
        
        super().update(tilemap, movement = movement)

        
