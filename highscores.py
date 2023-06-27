import random
import pygame
import os
import subprocess

pygame.init()

screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Mini-Game Hub")

font = pygame.font.Font(None, 60)
font2 = pygame.font.Font(None, 30)

width = screen.get_width()
height = screen.get_height()
splash_page = pygame.image.load('images/high.png')
scaled_splash = pygame.transform.scale(splash_page, (800, 800))

running = True

clock = pygame.time.Clock()



achieved_color = (0, 128, 0)
unachieved_color = (128, 128, 128)
with open("money.txt") as f:
    contents = f.readlines()
money=""
for thing in contents:
    money+=thing
money=int(money)


with open("highscores.txt") as z:
    c = z.readlines()
for g in c:
    x=c.index(g)
    c[x]=g.strip()
    c[x]=float(c[x])

achievements = [
    {"name": "Maple Rush: "+str(c[0])},
    {"name": "Galactic Gourds: "+str(c[2])},
    {"name": "Acorn Ascend: "+str(c[4])},
    {"name": "Sweater Weather Treats: "+str(c[5])},
    {"name": "Pumpkin Python: "+str(c[6])},
    {"name": "Fall Fury: "+str(c[7])},
    
]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos[0]>235 and mouse_pos[0]<445 and mouse_pos[1]>365 and mouse_pos[1]<460):
                    subprocess.Popen("python intro.py")
                    pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    txt = font.render("Money: " + str(money), 1, (0, 0, 0))

    scaled_splash = pygame.transform.smoothscale(scaled_splash, (width, height))

    screen.blit(scaled_splash, (0, 0))

    screen.blit(txt, (10, 10))

    y = 200
    for index, achievement in enumerate(achievements):
        name = achievement["name"]
        txt_achieve = font2.render(name, 1, unachieved_color)
        screen.blit(txt_achieve, (750, y))
        
        y += 80

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
