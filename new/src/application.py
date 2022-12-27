import pygame
import sys
from spritesheets import Spritesheet
from random import randint
import _random
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_w,
    K_s,
    QUIT,
)

count=0

BALL_RECT= int(10*2**0.5)
def collision(dx,dy,ball,rect):
    if dx>0:
        delta_x=ball.right-rect.left
    else:
        delta_x=rect.right-ball.left
    if dy>0:
        delta_y=ball.bottom-rect.top
    else:
        delta_y=rect.bottom-ball.top

    if abs(delta_x-delta_y)<10:
        dx*=-1
        dy*=-1
    else:
        if delta_x<delta_y:
            dx*=-1
        else:
            dy*=-1
    return dx,dy
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        self.surf=pygame.Surface((120,10))
        self.surf.fill("white")
        self.rect=self.surf.get_rect()
        self.rect.x=400-60
        self.rect.y=600-20

    def update(self,key_pressed):
        if key_pressed[K_RIGHT] and self.rect.right<800:
            self.rect.right+=10
        if key_pressed[K_LEFT] and self.rect.left>0:
            self.rect.left-=10
class Block(pygame.sprite.Sprite):
    def __init__(self,i,j):
        global block_color,block_color1
        
        self.hit=randint(0,1)
        self.color=randint(0,2)
        if self.hit==0:
         self.surf=block_color[self.color]
        else:
            self.surf=block_color1[self.color]
        self.rect=self.surf.get_rect()
        self.rect.x=10+90*i
        self.rect.y=10+65*j
    def update(self):
        global block_color,block_color1 
        if self.hit==0:
            self.hit=1   
        if self.hit==1:
            self.surf=block_color1[self.color]
            self.hit==0
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        global BALL_RECT
        self.surf=pygame.Surface((BALL_RECT,BALL_RECT))
        self.surf.fill("white")
        self.rect=self.surf.get_rect()
        self.rect.x=randint(BALL_RECT,800-BALL_RECT)
        self.rect.y=300
        self.dx=1
        self.dy=-1
    def update(self):
        ball.rect.x+=5*self.dx
        ball.rect.y+=5*self.dy

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

size=SCREEN_WIDTH,SCREEN_HEIGHT

pygame.init()

time=pygame.time.Clock()

fps=30
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Breakout")

my_spritesheet=Spritesheet(r"new\img\Sprite Sheet\Breakout_Tile_Free.png")

paddle_image=my_spritesheet.get_sprite(1158,396,243,64)
paddle_image=pygame.transform.scale(paddle_image,(120,10))
paddle=Paddle()
ball_image=my_spritesheet.get_sprite(1403,652,64,64)

ball_image=pygame.transform.scale(ball_image,(BALL_RECT,BALL_RECT))
blue=my_spritesheet.get_sprite(772,390,384,128)
blue=pygame.transform.scale(blue,(80,30))

red=my_spritesheet.get_sprite(772 ,260 ,384 ,128)
red=pygame.transform.scale(red,(80,30))

green=my_spritesheet.get_sprite(0 ,130,384,128)
green=pygame.transform.scale(green,(80,30))

blue_1=my_spritesheet.get_sprite(0 ,0 ,384,128)
blue_1=pygame.transform.scale(blue_1,(80,30))

red_1=my_spritesheet.get_sprite(772 ,130 ,384 ,128)
red_1=pygame.transform.scale(red_1,(80,30))

green_1=my_spritesheet.get_sprite(0 ,260 ,384,128)
green_1=pygame.transform.scale(green_1,(80,30))

block_color=[red,blue,green]
block_color1=[red_1,blue_1,green_1]
ball=Ball()
block_list=[Block(i,j) for i in range(9) for j in range(4)]



while True:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    key=pygame.key.get_pressed()
    paddle.update(key)
    ball.update()

    if ball.rect.centerx>800-BALL_RECT or ball.rect.centerx<BALL_RECT:
        ball.dx*=-1
    if ball.rect.y<BALL_RECT and ball.dy<0:
        ball.dy*=-1

    if ball.rect.colliderect(paddle.rect) and ball.dy>0:
        ball.dx,ball.dy=collision(ball.dx,ball.dy,ball.rect,paddle.rect)
    screen.blit(paddle_image,paddle.rect)
    screen.blit(ball_image,ball.rect)  
    
    for b in block_list:
        #b=block_rect[i]
        screen.blit(b.surf,b.rect)
   # [screen.blit(bb[1],b[1]) for b in enumerate(block_rect) for bb in enumerate(block_list)]

    hit_index=ball.rect.collidelist(block_list)
    if hit_index!=-1:
        
        hit_block=block_list[hit_index]
        hit_rect=hit_block.rect
        hit=hit_block.hit
        if hit==0:
            hit_block.update()

        else:
            block_list.pop(hit_index)    

        ball.dx,ball.dy=collision(ball.dx,ball.dy,ball.rect,hit_rect)
        fps+=2

    pygame.display.flip()
    time.tick(fps)