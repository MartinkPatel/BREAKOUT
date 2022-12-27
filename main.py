import pygame
from random import randint
import sys

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

pygame.init()

fps=pygame.time.Clock()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

size= SCREEN_WIDTH,SCREEN_HEIGHT
screen=pygame.display.set_mode(size)
pygame.display.set_caption("BREAKOUT")

PADDLE_SIZE=(120,10)

paddle=pygame.Rect(SCREEN_WIDTH/2 - PADDLE_SIZE[0]/2,SCREEN_HEIGHT-PADDLE_SIZE[1]-20,PADDLE_SIZE[0],PADDLE_SIZE[1])

BALL_RADIUS=10

BALL_RECT= int(BALL_RADIUS*2**0.5)

PADDLE_SPEED=10
ball_speed=5
dx,dy= 1,-1
ball=pygame.Rect(randint(BALL_RECT,SCREEN_WIDTH-BALL_RECT),SCREEN_HEIGHT/2,BALL_RECT,BALL_RECT)

block_list=[pygame.Rect(10+85*i,10+65*j,75,55) for i in range(10) for j in range (4)]
color_list=[(randint(30,255),randint(30,255),randint(30,255)) for i in range(10) for j in range (4)]

print(block_list[0])

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
while True:
    screen.fill("black")
    #MOUSE_POS=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            sys.exit()

    

    [pygame.draw.rect(screen,color_list[color],block) for color,block in enumerate(block_list)] 
    pygame.draw.rect(screen,"white",paddle)
    pygame.draw.circle(screen,"red",ball.center,BALL_RADIUS)
    key=pygame.key.get_pressed()
    #print(paddle.left,paddle.right)
    if key[pygame.K_RIGHT] and paddle.right<SCREEN_WIDTH:
        paddle.right+=PADDLE_SPEED
    if key[pygame.K_LEFT] and paddle.left>0: 
        paddle.left-=PADDLE_SPEED

    if ball.centerx<BALL_RADIUS or ball.centerx>SCREEN_WIDTH-BALL_RADIUS:
        dx*=-1

    if ball.centery<BALL_RADIUS:
        dy*=-1    

    if ball.colliderect(paddle) and dy>0:
        dx,dy=collision(dx,dy,ball,paddle)

    hit_index=ball.collidelist(block_list)
    if hit_index!=-1:
        hit_rect=block_list.pop(hit_index)
        hit_color=color_list.pop(hit_index)
        dx,dy=collision(dx,dy,ball,hit_rect)
        hit_rect.inflate_ip(ball.width*2,ball.height*2)
        pygame.draw.rect(screen,hit_color,hit_rect)
    ball.x+=ball_speed*dx
    ball.y+=ball_speed*dy

    if ball.centery >SCREEN_HEIGHT:
        dy*=-1
    

    pygame.display.flip()
    fps.tick(60)