import pygame
import sys 
from random import randint
from pygame import mixer
import os

def draw_sky():
    screen.blit(sky_surface,(skypos,0))
    screen.blit(sky_surface,(skypos+800,0))

def draw_floor():
    screen.blit(ground_surface,(floarpos,300))
    screen.blit(ground_surface,(floarpos+800,300))

def collision(player,obstricle):
    if obstricle:
        for obstricle_rectangle in obstricle:
            if player.colliderect(obstricle_rectangle):
                gameover_sound.play()                
                return False
    return True

def display_score():
    
    current_time=int(pygame.time.get_ticks()/1000)-start_time
    score_surface=text.render(f"Score : {current_time}",False,(64,64,64))
    score_rectangle=score_surface.get_rect(center=(700,50))
    screen.blit(score_surface,score_rectangle)
    
    return current_time

def obstricle_movement(obstricle_list):
    if obstricle_list:
        for obstricle_rectangle in obstricle_list:
            obstricle_rectangle.x-=5
            if obstricle_rectangle.bottom==300:
                screen.blit(snail_surface,obstricle_rectangle)
            elif obstricle_rectangle.bottom==200:
                screen.blit(fly_surface,obstricle_rectangle)
        
        obstricle_list=[obstricle for obstricle in obstricle_list if obstricle.x>-100] #imp
        return obstricle_list
    else:
            return []


def player_animation():
    global player_surface,player_index
    if player_rectangle.bottom<300:
        player_surface=player_jump
    else:
        player_index+=0.1
        if player_index>= len(player_walk):
            player_index=0
        player_surface=player_walk[int(player_index)]

mixer.init()
jump=pygame.mixer.Sound(os.path.join("audio","jump.mp3"))
bg=pygame.mixer.Sound(os.path.join("audio","music.wav"))
gameover_sound=pygame.mixer.Sound(os.path.join("audio","gameover.wav"))
bg.play(-1)
start_time=0
floarpos=0
skypos=0
xp=0  
score=0  
    
pygame.init()
screen=pygame.display.set_mode((800,400))
pygame.display.set_caption("Save the Runner")
pygame.display.set_icon(pygame.image.load(os.path.join("icon","icon.svg")))
clock =pygame.time.Clock()
game_active=True
text=pygame.font.Font(os.path.join("font","Pixeltype.ttf"),50)
#sky and ground surface
sky_surface=pygame.image.load(os.path.join("graphics","Sky.png")).convert()
ground_surface=pygame.image.load(os.path.join("graphics","ground.png")).convert()

obstricle_rectangle_list=[]

#snail
snail_surface_frame1=pygame.image.load(os.path.join("graphics\\snail","snail1.png")).convert_alpha()
snail_surface_frame1=pygame.transform.rotozoom(snail_surface_frame1,0,0.72)
snail_surface_frame2=pygame.image.load(os.path.join("graphics\\snail","snail2.png")).convert_alpha()
snail_surface_frame2=pygame.transform.rotozoom(snail_surface_frame2,0,0.72)
snail_frame=[snail_surface_frame1,snail_surface_frame2]
snail_index=0
snail_surface=snail_frame[snail_index]

#fly surface
fly_surface_frame1=pygame.image.load(os.path.join("graphics\\Fly","Fly1.png"))
fly_surface_frame2=pygame.image.load(os.path.join("graphics\\Fly","Fly2.png"))
fly_frame=[fly_surface_frame1,fly_surface_frame2]
fly_index=0
fly_surface=fly_frame[fly_index]

#player urface
player_walk1=pygame.image.load(os.path.join("graphics\\Player","player_stand.png")).convert_alpha()
player_walk2=pygame.image.load(os.path.join("graphics\\Player","player_walk_1.png")).convert_alpha()
player_walk3=pygame.image.load(os.path.join("graphics\\Player","player_walk_2.png")).convert_alpha()
player_walk=[player_walk3,player_walk2,player_walk1]
player_index=0
player_jump=pygame.image.load(os.path.join("graphics\\Player","jump.png")).convert_alpha()
player_surface=player_walk[player_index]
player_rectangle=player_surface.get_rect(midbottom=(80,300))
player_gravity=0


# game over player 
player_stand=pygame.image.load(os.path.join("graphics\\Player","player_stand.png")).convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle=player_stand.get_rect(center=(400,200))

#game name
game_name=text.render("Pixel Runner",False,"blue")
game_name_rectangle=game_name.get_rect(center=(400,50))

#game message 
game_message=text.render("Press Y to run ",False,(111,196,169))
game_message_rectangle=game_message.get_rect(center=(400,80))

# game timer
obsticle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obsticle_timer,1600)

#snail timer
snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,600)

#fly timer
fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)
run=True
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            
                   
               
        if event.type==pygame.KEYDOWN and game_active:
            if event.key==pygame.K_SPACE and player_rectangle.bottom >=300:            
                player_gravity=-20
                jump.play()
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_y:
                game_active=True
               
                xp=0
                start_time=int(pygame.time.get_ticks()/1000)               

       
        if event.type==obsticle_timer and game_active:
            if randint(0,2)==0:
                obstricle_rectangle_list.append(snail_surface.get_rect(bottomright=((randint(900,1100),300))))
            elif randint(0,2)==1:
                
                obstricle_rectangle_list.append(fly_surface.get_rect(bottomright=((randint(900,1100),200))))
        
        if game_active and event.type ==snail_animation_timer:
            if snail_index==0:
                snail_index=1
                
            elif snail_index==1:
                snail_index=0
                
            snail_surface=snail_frame[snail_index]
        if game_active and event.type ==fly_animation_timer:
            if fly_index==0:
                fly_index=1
            elif fly_index==1:
                fly_index=0
            fly_surface=fly_frame[fly_index]

    if game_active:
        skypos-=(0.1+(xp/10))
        draw_sky()
        if skypos<=-800:
            skypos=0
        floarpos=floarpos-(1+xp)
        draw_floor()
        if floarpos<=-800:
            floarpos=0
        
       
        score=display_score()
        if score/10==0:
           xp+=0.05       
  
        player_gravity+=1
        player_rectangle.y+=player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom=300
       
        player_animation()
        screen.blit(player_surface,player_rectangle)

        obstricle_rectangle_list=obstricle_movement(obstricle_rectangle_list)

        
        game_active=collision(player_rectangle,obstricle_rectangle_list)
    else:
        if game_active==False:
            screen.fill((94,129,162))
            obstricle_rectangle_list.clear()
           
            player_gravity=0 
            xp=0
            screen.blit(game_name,game_name_rectangle)
            screen.blit(game_message,game_message_rectangle)
            score_message=text.render(f"Your Score : {score}",False,(111,196,169))
            score_message_rectangle=score_message.get_rect(center=(400,350))
                      
            screen.blit(player_stand,player_stand_rectangle)
            if score==0:                
                screen.blit(game_message,game_message_rectangle)
            else:
                screen.blit(score_message,score_message_rectangle)   
    
    pygame.display.update()
    clock.tick(60+xp)
pygame.quit()
