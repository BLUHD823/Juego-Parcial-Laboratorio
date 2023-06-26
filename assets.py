from typing import Any
import pygame, sys 
from pygame.locals import *
from pygame.sprite import Group

class Paleta(pygame.sprite.Sprite):
    
    def __init__(self, posicion,velocidad,diccionario,diccionario_girado,gravedad,salto_distancia) -> None:
        super().__init__()
        self.sprit_girado = diccionario_girado # {'idle_animation':[4],'walking_animation':[4],''jumping_animation':[2]'}
        self.sprit = diccionario # {'idle_animation':[4],'walking_animation':[4],''jumping_animation':[2]'}
        self.image = diccionario['idle_animation'][0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = posicion
        self.mask = pygame.mask.from_surface(self.image)
        self.direction = pygame.math.Vector2(0,0)
        self.velocidad_x = velocidad
        self.gravity = gravedad
        self.jump_speed = salto_distancia
        self.direccion = 'RIGHT'
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.invincible = False
        self.invincibility_duration = 400
        self.hurt_time = 0
        self.life = 3

    def status_animation(self,display):
        direccion = None
        if self.direccion == 'RIGHT':
            direccion = self.sprit
        elif self.direccion == 'LEFT':
            direccion = self.sprit_girado
        if self.direction.y > 0:
            self.status = 'falling'
        if self.direction.y < 0:
            self.status = 'jumping'

        if self.status == 'idle':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['idle_animation']):
                self.frame_index = 0
            self.image = direccion['idle_animation'][int(self.frame_index)]
            display.blit( self.image,self.rect)
                
        if self.status == 'walking':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['walking_animation']):
                self.frame_index = 0
            self.image = direccion['walking_animation'][int(self.frame_index)]
            display.blit( self.image,self.rect)

        if self.status == 'jumping':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['jumping_animation']):
                self.frame_index = 0
            self.image = direccion['jumping_animation'][int(self.frame_index)]
            display.blit( self.image,self.rect)

        if self.status == 'falling':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['falling_animation']):
                self.frame_index = 0
            self.image = direccion['falling_animation'][int(self.frame_index)]
            display.blit( self.image,self.rect)
    def mover_x_izq(self):
        self.direccion = "LEFT"
        self.status = "walking"
        if self.rect.left > 0:
            self.direction.x = -1  
            self.posicion = self.rect.midbottom
        else:
            self.rect.left = 0   
    def mover_x_derecha(self,WIDTH):
        self.direccion = "RIGHT"
        self.status = "walking"
        if self.rect.right < WIDTH:
            self.direction.x = 1        
            self.posicion = self.rect.midbottom
        else:
            self.rect.right = WIDTH   
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.rect.y += self.gravity
    def salto(self):
        self.direction.y = self.jump_speed
    def get_damage(self):
        if  self.invincible == False:
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.life -= 1
            print(self.life)
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False
                
    def draw(self,display):
        self.status_animation(display)
    def update(self,display):
        self.draw(display)
        self.rect.x += self.direction.x * 5
        self.invincibility_timer()
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self,dict_l,dict_r,position,velocity,right,left) -> None:
        super().__init__()
        self.sprites = dict_r
        self.sprites_left = dict_l
        self.surface = self.sprites['idle_animation'][0]
        self.rect = self.surface.get_rect()
        self.rect.midbottom = position
        self.mask = pygame.mask.from_surface(self.surface)
        self.direction = pygame.math.Vector2(0,0)
        self.velocity = velocity
        self.old_velocity = velocity
        self.status = 'walking'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.right_limit = right[0]
        self.left_limit = left[0]
        self.orientation = 'right'
        self.dead = False
       

    def animate(self,display):
        direccion = None
        if self.orientation ==  'right':
            direccion = self.sprites  
        else:
            direccion = self.sprites_left
            

        if self.status == 'walking':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['walking_animation']):
                    self.frame_index = 0
            self.surface = direccion['walking_animation'][int(self.frame_index)]
            display.blit( self.surface,self.rect)
        if self.status == 'death':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['death_animation']):
                self.frame_index = 0
                self.dead  = True
            self.surface = direccion['death_animation'][int(self.frame_index)]
            display.blit( self.surface,self.rect)
        if self.status == 'attack':
            self.frame_index += self.animation_speed
            if self.frame_index >= len(direccion['attack_animation']):
                self.frame_index = 0
                self.dead = False
                self.velocity = self.old_velocity
                
            self.surface = direccion['attack_animation'][int(self.frame_index)]
            display.blit( self.surface,self.rect)
           
    def move(self):
        self.rect.x += self.velocity
        if self.rect.right >= self.right_limit:
            self.velocity *= -1
            self.orientation = 'left'
            self.status = 'walking'
        if self.rect.left <= self.left_limit:
            self.velocity *= -1
            self.orientation = 'right'
            self.status = 'walking'
            

    def update(self,display):
        self.move()
        self.animate(display)
        
        # display.blit(self.surface,self.rect)





class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, posicion,path) -> None:
        super().__init__()
        self.surface = pygame.image.load(path)
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = posicion
        self.mask = pygame.mask.from_surface(self.surface)
        self.posicion = posicion
    def draw(self,display):
        display.blit(self.surface, self.rect)
    
class Piso(pygame.sprite.Sprite):
    def __init__(self,posicion) -> None:
        super().__init__()
        self.surface = pygame.image.load('./src/tile definitivo.png')
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = posicion
        self.mask = pygame.mask.from_surface(self.surface)
        self.posicion = posicion
    

class Options(pygame.sprite.Sprite):
    def __init__(self,posicion,path) -> None:
        super().__init__()
        self.surface = path
        self.rect = self.surface.get_rect()
        self.rect.midbottom = posicion
        self.mask = pygame.mask.from_surface(self.surface)
        self.clicked = False
    def draw(self,display):
        action =  False
        #sacar la posición del mouse
        pos = pygame.mouse.get_pos()

        #acciones del mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        display.blit(self.surface,self.rect)
        return action

        
        