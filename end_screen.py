import pygame
import os
import subprocess

pygame.init()
screen= pygame.display.set_mode()
pygame.display.set_caption('Minigames')

clock = pygame.time.Clock()
font = pygame.font.Font('images/Neucha-Regular.ttf',60)
font1 = pygame.font.Font('images/PermanentMarker-Regular.ttf', 90)

color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
width = screen.get_width()
height = screen.get_height()
smallfont = pygame.font.SysFont('Arial',35)
text = smallfont.render('S T A R T' , True , color)


splash_page = pygame.image.load('images/dead.png')

scaled_splash = pygame.transform.scale(splash_page, (800, 800))


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)
counter=1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            subprocess.Popen("python intro.py")
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                break

                

    scaled_splash = pygame.transform.smoothscale(scaled_splash, (width, height)) 

    screen.blit(scaled_splash,(0,0))
    

         
    pygame.display.update()
    clock.tick(60)
pygame.quit()