import pygame
import sys
from spritesheets import Spritesheet
from random import randint
import _random
import random
from button import Button
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
fontt=pygame.font.SysFont(r"new\font\CANDY___.otf",90)

count=0
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

size=SCREEN_WIDTH,SCREEN_HEIGHT
pygame.mixer.init()
pygame.init()

time=pygame.time.Clock()
background_sound=pygame.mixer.Sound(r"new/sounds/background.mp3")
#ppaddle_color=pygame.mixer.Sound(r"new/sounds/paddle.m4a")
#brick_sound=pygame.mixer.Sound(r"new/sounds/brick.m4a")
#wall_sound=pygame.mixer.Sound(r"new/sounds/wall.m4a")
hit_sound=pygame.mixer.Sound(r"new/sounds/hit.mp3")
fps=30
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Breakout")

my_spritesheet=Spritesheet(r"new\img\Sprite Sheet\Breakout_Tile_Free.png")

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

sound_on=True

def sound_check():
    global sound_on
    if sound_on==True:
        sound=pygame.image.load(r"new/img/sound.png")
        sound=pygame.transform.scale(sound,(30,30))
    if sound_on== False:
        sound=pygame.image.load(r"new/img/mute.png")
        sound=pygame.transform.scale(sound,(30,30))
    #sound_rect=sound.get_rect(center=(600,400))
    return sound

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
        self.rect.x+=5*self.dx
        self.rect.y+=5*self.dy


def win_check(win):
    if win==True:
        screen.fill("black")
        text=fontt.render("YOU WIN !",True,"white")
        screen.blit(text,(300,300))
        
        
    else:
        screen.fill("black")
        text=fontt.render("YOU LOSE !",True,"white")
        screen.blit(text,(300,300))
        

    pygame.display.flip()
    pygame.time.wait(2000)
    menu()    

def play():
    global ppaddle_color,wall_sound,brick_sound,hit_sound
    my_spritesheet=Spritesheet(r"new\img\Sprite Sheet\Breakout_Tile_Free.png")
    score=0
    paddle_image=my_spritesheet.get_sprite(1158,396,243,64)
    paddle_image=pygame.transform.scale(paddle_image,(120,10))
    paddle=Paddle()
    ball_image=my_spritesheet.get_sprite(1403,652,64,64)

    ball_image=pygame.transform.scale(ball_image,(BALL_RECT,BALL_RECT))
    

    
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
            hit_sound.play()
        if ball.rect.y<BALL_RECT and ball.dy<0:
            ball.dy*=-1
            hit_sound.play()

        if ball.rect.colliderect(paddle.rect) and ball.dy>0:
            ball.dx,ball.dy=collision(ball.dx,ball.dy,ball.rect,paddle.rect)
            hit_sound.play()
        screen.blit(paddle_image,paddle.rect)
        screen.blit(ball_image,ball.rect)  
        if ball.rect.centery>600-BALL_RECT:
            win_check(False)
        for b in block_list:
            #b=block_rect[i]
            screen.blit(b.surf,b.rect)
    # [screen.blit(bb[1],b[1]) for b in enumerate(block_rect) for bb in enumerate(block_list)]

        hit_index=ball.rect.collidelist(block_list)
        if hit_index!=-1:
            hit_sound.play()
            hit_block=block_list[hit_index]
            hit_rect=hit_block.rect
            hit=hit_block.hit
            if hit==0:
                hit_block.update()

            else:
                block_list.pop(hit_index)
                score+=1    

            ball.dx,ball.dy=collision(ball.dx,ball.dy,ball.rect,hit_rect)
            if score==36:
                win_check(True)
            global fps
            fps+=2
        font1=pygame.font.SysFont(r"new\font\CANDY___.otf",30)    
        textt=font1.render("score={} ".format(score),True,"white")
        screen.blit(textt,(700,550))
        pygame.display.flip()
        time.tick(fps)

def menu():
    global background_sound
    global sound_on
    screen.fill("black")
    running =True
    if sound_on:
        background_sound.play(loops=-1)
    while running:
       
        
        MENU_MOUSE_POS=pygame.mouse.get_pos()
        menu_text=fontt.render("MAIN MENU",True,"white")
        menu_rect=menu_text.get_rect(center=(400,150))
        screen.blit(menu_text,menu_rect)    
        
        PLAY_BUTTON=Button(image=None,pos=(400,300),text_input="PLAY",font=fontt,base_colour="white",hovering_colour="red")
        QUIT_BUTTON=Button(image=None,pos=(400,400),text_input="QUIT",font=fontt,base_colour="white",hovering_colour="red")
        SOUND_BUTTON=Button(image=sound_check(),pos=(700,500),text_input="",font=fontt,base_colour="white",hovering_colour="white")
        for button in PLAY_BUTTON,QUIT_BUTTON,SOUND_BUTTON:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)  


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    background_sound.stop()
                    play()
                if SOUND_BUTTON.checkForInput(MENU_MOUSE_POS):
                    black_image=pygame.image.load(r"new/img/black.png")
                    black_image=pygame.transform.scale(black_image,(30,30))
                    screen.blit(black_image,SOUND_BUTTON.rect)
                    if sound_on:
                        sound_on=False
                        background_sound.stop()
                    else: 
                        sound_on=True    
                        background_sound.play()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()      

        pygame.display.flip()
        global fps
        time.tick(fps)
menu()