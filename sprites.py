from shutil import move
import pygame
from utils import Timer
COYOTE_JUMP_EVENT = pygame.USEREVENT + 1
BLINK_LIGHT_EVENT = pygame.USEREVENT + 2 
INVINCIBILITY_EVENT = pygame.USEREVENT + 3


class Body(pygame.sprite.Sprite):
    def __init__(self,game,pos,size,color):
        self.game = game
        self.pos = pos
        self.size = size
        self.velocity = [0,0]
        self.display = pygame.Surface(self.size)
        self.display.fill(color) 
        self.collisions = {'up':False, 'down':False, 'left':False, 'right':False}
        self.sides = {'right':False, 'left':False}
        
        
        self.was_on_floor = False
        self.coyote = False
        self.timer = Timer(1000)
        
        self.y = 0

    def rect(self):
        return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])

    def update(self,tilemap,movement, offset=[0,0]):
        
        
        self.collisions = {'up':False, 'down':False, 'left':False, 'right':False}
       
        self.apply_gravity()
        
        framemove = (self.velocity[0] + movement[0], self.velocity[1] + movement[1])
        self.check_sides(framemove)
        self.framemove = framemove
        self.pos[0] += framemove[0]
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
         
            if body_rect.colliderect(rect):
                
                if framemove[0] > 0:
                    body_rect.right = rect.left
                    self.collisions['right'] = True
                    
                    
                    
                    
                if framemove[0] < 0:
                    body_rect.left = rect.right
                    self.collisions['left'] = True
                    


                self.pos[0] = body_rect.x
        
        
        

        
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
        
        
     
 



    def render(self,surf,offset = (0,0)):
        rect = self.rect()
        surf.blit(self.display, 
                  (rect[0] - offset[0], rect[1] - offset[1]))
        
    def check_sides(self, framemove):
        if framemove[0] < 0:
            self.sides['left'] =  True
            self.sides['right'] =  False
        
        elif framemove[0] > 0:
            self.sides['left'] =  False
            self.sides['right'] =  True

        

class player(Body):
    def __init__(self, game, pos, size, color):
        super().__init__(game, pos, size, color)
        self.jump_value = 1
        
        self.jumps = self.jump_value

        self.status = 'normal'

        self.lives= 3

        self.can_collide = True


        

    
        

    def update(self,tilemap, movement):
        
        self.can_coyote()
        self.into_light(tilemap)
        
        self.enemy_collide()
    
        

        
        super().update(tilemap, movement = movement)
        

    def jump(self):
        if self.jumps > 0: 
            self.velocity[1] =-7
            self.jumps -=1
           

    def into_light(self, tilemap):
        body_rect = self.rect()
        for tile in tilemap.light_detect(self.pos):
        
            if body_rect.colliderect(tile['rect']) and tile['visible']:
                self.status = 'detected'
                
            elif not body_rect.colliderect(tile['rect']):
                self.status = 'normal'
 
    
    def can_coyote(self):

        if not self.collisions['down'] and self.was_on_floor and self.velocity[1] >= 0:
            
            pygame.time.set_timer(COYOTE_JUMP_EVENT, 500)
        if not self.collisions['down']:
                self.was_on_floor = False

    def enemy_collide(self):
        enemies = [enemy for enemy in self.game.enemies]
        rect = self.rect()
        enemy_collision = {'up':False, 'down':False, 'left':False, 'right':False}
        
        

       
        for enemy in enemies:
            if rect.colliderect(enemy.rect()) and enemy.visible and self.can_collide:
                self.hp()
                if self.sides['left']:
                    rect.left = enemy.rect().right

                    self.pos[0] = rect.x + 10
                    self.pos[1] -= 30
                
                if self.sides['right']:
                    rect.right = enemy.rect().left

                    self.pos[0] = rect.x - 10
                    self.pos[1] -= 30
                

    

    def flip(self):
        self.flip = not self.flip

    

    def coyote_timer(self):
                
        self.timer.activate()
        self.timer.update()
        
        

        if self.timer.active:
            print('why')

    def hp(self):
        self.lives -= 1
        print(self.lives)
        self.can_collide = False
        pygame.time.set_timer(INVINCIBILITY_EVENT, 5000)





 

                    
            


        
class Enemy(Body):
    def __init__(self, game, pos, size, color):
        super().__init__(game, pos, size, color)
        self.jump_value = 1
        self.visible = True
        self.bound = True
        self.move = 1
    
    def update(self, tilemap, movement = [0,0], offset=[0, 0]):
        self.in_the_light(tilemap)
        self.out_of_light(tilemap)
        self.pos[0] += self.move
        
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
         
            if body_rect.colliderect(rect):
                
                if self.move > 0:
                    body_rect.right = rect.left
                    self.collisions['right'] = True
                    
                    
                    
                    
                if self.move < 0:
                    body_rect.left = rect.right
                    self.collisions['left'] = True

                self.move *=-1
                    


                self.pos[0] = body_rect.x
        
        
        
        
        return super().update(tilemap, movement, offset)
    
    def render(self,surf,offset = (0,0)):
        if self.visible and self.game.player.status == 'detected':
            rect = self.rect()
            surf.blit(self.display, 
                    (rect[0] - offset[0], rect[1] - offset[1]))
            


    def in_the_light(self, tilemap):
        enemy_rect = self.rect()
        
        for tile in tilemap.light_detect(self.pos):
            if enemy_rect.colliderect(tile['rect']) and tile['visible']:
                self.visible = True
   

            if enemy_rect.colliderect(tile['rect']) and not tile['visible']:
           
                
                self.visible = False

    def out_of_light(self,tilemap):
        enemy_rect = self.rect()
        

        for tile in tilemap.light_detect(self.pos):
            if  not enemy_rect.colliderect(tile['rect']):
                self.bound = False
                
                
            else:
                self.bound = True
        if not self.bound :
            self.move *= -1

            

        



            


            

           
            