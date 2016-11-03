import pygame
from pygame.locals import *
import random
import time

pygame.init()

pygame.display.set_caption("Super Mario")

font = pygame.font.SysFont("comicsansms", 72)
font1 = pygame.font.SysFont("arial", 20)
font2 = pygame.font.SysFont("bodoni", 36)


width=640
length=480
screen = pygame.display.set_mode((width,length), 0 ,32)
intro_background=pygame.image.load("intro.jpg")
background=pygame.image.load("background.jpg")
clouds=pygame.image.load("clouds.png")
ground=pygame.image.load("ground.jpg")
lava=pygame.image.load("lava.jpg")
mario_icons_right=[pygame.image.load("mario_running_right_1.jpg"),pygame.image.load("mario_running_right_2.jpg")]
mario_icons_left=[pygame.image.load("mario_running_left_1.jpg"),pygame.image.load("mario_running_left_2.jpg")]
mario_icons_standing=[pygame.image.load("mario_standing_1.png"),pygame.image.load("mario_standing_2.jpg")]
mario_icons_jumping=[pygame.image.load("mario_right_jump.jpg"),pygame.image.load("mario_left_jump.jpg")]
pipes=[pygame.image.load("pipe_small.jpg"),pygame.image.load("pipe.jpg")]
box=[pygame.image.load("box.jpg"),pygame.image.load("box1.jpg")]

enemy=pygame.image.load("enemy.jpg")
enemy_right=pygame.image.load("enemy_right.jpg")
enemy2=pygame.image.load("enemy2.jpg")
canon=pygame.image.load("canon.jpg")
finish=pygame.image.load("finish.png")
finish_flag=pygame.image.load("finish_flag.png")

pipes_list=[[400,0],[600,1],[700,0],[900,1],[1100,1], [1500,0], [1800,0],[2000,1]]
box_list=[[-200,300,1],[-250,300,1],[-300,300,1],[400,300,0],[400,250,0],[450,300,0],[450,250,1],[500,300,0],[500,250,0],[1100,400,0],[1150,400,1],[1200,400,0],[1100,350,0],[1150,350,0],[1200,350,0], [1400,300,0],[1400,250,0],[1450,300,0],[1450,250,1],[1500,300,0],[1500,250,0],[2850,72,0],[2900,72,0]]

click_sound= pygame.mixer.Sound("click1.wav")
bam_sound= pygame.mixer.Sound("bloop3.wav")




def intro():
    while True:
        screen.blit(intro_background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == KEYDOWN:
                start()
        pygame.display.update()


def mario(x_move,movement,stability,ground_x, mario_y_move,mario_y_position):
    if x_move==-1:
        if mario_y_move>0:
            screen.blit(mario_icons_jumping[1],(width/3,mario_y_position))
        else:
            screen.blit(mario_icons_left[(movement/10)%2],(width/3,mario_y_position))
        
        
    elif x_move==1:
        if mario_y_move>0:
            screen.blit(mario_icons_jumping[0],(width/3,mario_y_position))
        else:
            screen.blit(mario_icons_right[(movement/10)%2],(width/3,mario_y_position))
        
    else:
        if mario_y_move>0:
            screen.blit(mario_icons_jumping[0],(width/3,mario_y_position))
        else:
            if stability%1000<600:
                screen.blit(mario_icons_standing[0],(width/3,mario_y_position))
            else:
                screen.blit(mario_icons_standing[1],(width/3,mario_y_position))

    screen.blit(ground,(ground_x,length-23))
    screen.blit(ground,(ground_x-640,length-23))
    screen.blit(ground,(ground_x+640,length-23))
    screen.blit(clouds,(ground_x,0))
    screen.blit(clouds,(ground_x-640,0))
    screen.blit(clouds,(ground_x+640,0))

    
def check_collision(game_position,mario_y_position):
    collision=1 ###no collision
    for a in pipes_list:###pipes_list:
        if a[1]==0:
            if (-game_position+250>a[0]) and (-game_position+250<a[0]+100+39):
                if mario_y_position+67>length-86:
                    if -game_position+250<a[0]+4: ###left collision
                        collision=0
                    else:
                        collision=2
                    if -game_position+250>a[0]+5 and -game_position+250<a[0]+100+39-5:
                        collision=3
                else: pass#collision=5
        elif a[1]==1:
            if (-game_position+250>a[0]) and (-game_position+250<a[0]+100+39):
                if mario_y_position+67>length-86-40:
                    if -game_position+250<a[0]+4: ###left collision
                        collision=0
                    else:
                        collision=2
                    if -game_position+250>a[0]+5 and -game_position+250<a[0]+100+39-5:
                        collision=4
            
    return collision
    
        
    
def check_enemy(game_position,mario_y_position, enemy_x_position, enemy2_x_position):
    if game_position>240 and mario_y_position>389: ###checks the lava in the left of the screen at the beginning of the game
        time.sleep(.5)
        intro()
    if 1452>-game_position and -game_position>1105 and mario_y_position>389: ###checks the lava in the middle of the game
        time.sleep(.5)
        intro()

    
    if (abs(game_position - 190 + enemy2_x_position) < 3 or -180<game_position<-100) and mario_y_position >330:###checks collision with the canon
        time.sleep(.5)
        intro()

    pygame.display.update()


def start():
    e=True

    game_position=0
    ground_x=0
    x_move=0
    mario_y_position=length-67-23
    mario_y_before_jump=mario_y_position
    anodos=0
    
    movement=0 ###for mario movements
    stability=0###

    enemy_left_movement=True
    enemy_x_position=500
    enemy2_x_position=300
    
    pygame.mixer.Sound.play(bam_sound)
    
    jump=False

    
    while e:
        screen.blit(background,(0,0))
        #screen.blit(pygame.image.load("mario_small_right.jpg"),(width/3,length-81))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    x_move=-1
                if event.key == K_RIGHT:
                    x_move=1
                if event.key == K_SPACE and not jump:
                    pygame.mixer.Sound.play(click_sound)
                    ####To create a sound at the jump
                    jump=True
                    anodos=4
                    
                    
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    x_move=0
                if event.key == K_RIGHT:
                    x_move=0



        if mario_y_position>mario_y_before_jump:
            mario_y_position=mario_y_before_jump
            anodos=0
            jump=False
        
        mario_y_position-=anodos        
        if jump and mario_y_before_jump-mario_y_position>120:   ###70: ####jump maximum pixeles
            anodos=-3
            

        ###print mario_y_position
          
        if check_collision(game_position,mario_y_position)==1:
            mario_y_before_jump=length-67-23
            game_position=int(game_position)
            ground_x=int(ground_x)
            game_position+=x_move*(-4) ###### +to the right, - to the left
            ground_x+=x_move*(-4)
        elif check_collision(game_position,mario_y_position)==0:##left collision
            game_position+=.2
            ground_x+=.2
        elif check_collision(game_position,mario_y_position)==2:##right collision
            game_position-=.2
            ground_x-=.2

        elif check_collision(game_position,mario_y_position)==3:#######small pipe
            mario_y_before_jump=mario_y_position-1
            anodos=0
            jump=False
        elif check_collision(game_position,mario_y_position)==4:#####big pipe
            mario_y_before_jump=mario_y_position-1
            anodos=0
            jump=False


        if ground_x<=-640 or ground_x>=640:
            ground_x=0
        

        if x_move==0:
            stability+=1
        else:
            movement+=1
            stability=0

        
        mario(x_move,movement,stability,ground_x, mario_y_position-mario_y_before_jump,mario_y_position)

 
        for a in pipes_list:
            if a[1]==0: ###for the small pipe
                screen.blit(pipes[a[1]],(game_position+a[0],length-126+40))
            else: ###for the big pipe
                screen.blit(pipes[a[1]],(game_position+a[0],length-126))
        for a in box_list: ##for the boxes
            screen.blit(box[a[2]],(game_position+a[0],length-a[1]))

        screen.blit(finish,(game_position +2200 ,100))
        screen.blit(finish_flag,(game_position +2550 ,0))
        
        
        if game_position<-2400:
            intro()
        
        if enemy_left_movement:
            screen.blit(enemy,(game_position + 50+ enemy_x_position,425))
            screen.blit(enemy,(game_position + 550+ enemy_x_position,425))
            screen.blit(enemy,(game_position + 1450+ enemy_x_position,425))
            enemy_x_position-=1
        else:
            screen.blit(enemy_right,(game_position + 50+ enemy_x_position,425))
            screen.blit(enemy_right,(game_position + 550+ enemy_x_position,425))
            screen.blit(enemy_right,(game_position + 1450+ enemy_x_position,425))
            enemy_x_position+=1
        if enemy_x_position<450 or enemy_x_position>521:
            enemy_left_movement=not(enemy_left_movement)


        screen.blit(enemy2,(game_position + 50 + enemy2_x_position,398))
        enemy2_x_position-=2
        if enemy2_x_position<-500:
            if game_position>-1000:
                pygame.mixer.Sound.play(bam_sound)
            enemy2_x_position = 300
            
        screen.blit(canon,(game_position + 350,398))



        screen.blit(enemy2,(game_position + 2540 + enemy2_x_position,398-50))
        enemy2_x_position-=2
        if enemy2_x_position<-430:
            pygame.mixer.Sound.play(bam_sound)
            enemy2_x_position = 300
    
        screen.blit(canon,(game_position + 2850,398-50))

        
        screen.blit(lava,(game_position-348,length-22)) ###lava in the beginning at the left of the game
        screen.blit(lava,(game_position+ 1348,length-22)) ###lava in the middle of the game

        check_enemy(game_position,mario_y_position, enemy_x_position,enemy2_x_position)

        
        
        pygame.display.update()



intro()
###pygame.display.update()

