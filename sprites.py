
import pygame
from utils import Timer
COYOTE_JUMP_EVENT = pygame.USEREVENT + 1

class Body(pygame.sprite.Sprite):
    def __init__(self,game,pos,size,color):
        self.game = game
        self.pos = pos
        self.size = size
        self.velocity = [0,0]
        self.display = pygame.Surface(self.size)
        self.display.fill(color) 
        self.collisions = {'up':False, 'down':False, 'left':False, 'right':False}
   
        
        self.was_on_floor = False
        self.coyote = False
        self.timer = Timer(1000)
        
        self.y = 0

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self,tilemap,movement, offset=[0,0]):
        self.can_coyote()
        self.collisions = {'up':False, 'down':False, 'left':False, 'right':False}
       
        self.apply_gravity()
        
        framemove = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        
        self.pos[0] += framemove[0]
        
        

        
        self.pos[1] += framemove[1] 
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
         
            if body_rect.colliderect(rect):
                
                if framemove[1] > 0:
                    body_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.y = body_rect.y
                    
                    self.jumps = self.jump_value
             
                    self.was_on_floor = True
                if framemove[1] < 0:
                    body_rect.top = rect.bottom
                    self.collisions['up'] = True


                self.pos[1] = body_rect.y
        
        
    
   


    def apply_gravity(self):
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
        
     
    def can_coyote(self):

      
        print(self.was_on_floor)

        if not self.collisions['down'] and self.was_on_floor and self.velocity[1] >= 0:
            
            pygame.time.set_timer(COYOTE_JUMP_EVENT, 500)
        if not self.collisions['down']:
                self.was_on_floor = False




    def coyote_timer(self):
                
        self.timer.activate()
        self.timer.update()
        
        

        if self.timer.active:
            print('why')




    def render(self,surf,offset = (0,0)):
        rect = self.rect()
        surf.blit(self.display, 
                  (rect[0] - offset[0], rect[1] - offset[1]))
        

class player(Body):
    def __init__(self, game, pos, size, color):
        super().__init__(game, pos, size, color)
        self.jump_value = 1
        
        self.jumps = self.jump_value
        

    def update(self,tilemap, movement):
     
    
        

        
        super().update(tilemap, movement = movement)
        

    def jump(self):
        if self.jumps > 0: 
            self.velocity[1] =-7
            self.jumps -=1
            print(self.jumps)
            
        
            


        
