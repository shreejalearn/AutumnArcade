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


width = screen.get_width()
height = screen.get_height()
splash_page = pygame.image.load('images/games.png')
scaled_splash = pygame.transform.scale(splash_page, (800, 800))


running = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0]>230 and mouse_pos[0]<440 and mouse_pos[1]>365 and mouse_pos[1]<460:
                    subprocess.Popen("python achievements.py")
                    pygame.quit()
                if mouse_pos[0]>230 and mouse_pos[0]<440 and mouse_pos[1]>475 and mouse_pos[1]<565:
                    subprocess.Popen("python highscores.py")
                    pygame.quit()
                if mouse_pos[0]>490 and mouse_pos[0]<850 and mouse_pos[1]>305 and mouse_pos[1]<400:
                    subprocess.Popen("python endless_runner.py")
                    pygame.quit()
                if mouse_pos[0]>490 and mouse_pos[0]<850 and mouse_pos[1]>450 and mouse_pos[1]<545:
                    subprocess.Popen("python tic_tac_toe.py")
                    pygame.quit()
                if mouse_pos[0]>490 and mouse_pos[0]<850 and mouse_pos[1]>610 and mouse_pos[1]<700:
                    subprocess.Popen("python space_invaders.py") 
                    pygame.quit()
                if mouse_pos[0]>900 and mouse_pos[0]<1260 and mouse_pos[1]>135 and mouse_pos[1]<230:
                    subprocess.Popen("python pong.py")
                    pygame.quit()
                if mouse_pos[0]>900 and mouse_pos[0]<1260 and mouse_pos[1]>265 and mouse_pos[1]<350:
                    subprocess.Popen("python flappy_bird.py")
                    pygame.quit()
                if mouse_pos[0]>900 and mouse_pos[0]<1260 and mouse_pos[1]>380 and mouse_pos[1]<470:
                    subprocess.Popen("python clicker.py")
                    pygame.quit()
                if mouse_pos[0]>900 and mouse_pos[0]<1260 and mouse_pos[1]>495 and mouse_pos[1]<585:
                    subprocess.Popen("python snakeworking.py")
                    pygame.quit()
                if mouse_pos[0]>900 and mouse_pos[0]<1260 and mouse_pos[1]>610 and mouse_pos[1]<700:
                    subprocess.Popen("python race.py")
                    pygame.quit()
                
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running=False
    with open("money.txt") as f:
        contents = f.readlines()
    c=""
    for thing in contents:
        c+=thing
    
    txt = font.render("Money: "+c, 1, (0,0,0))
    

    scaled_splash = pygame.transform.smoothscale(scaled_splash, (width, height))

    screen.blit(scaled_splash, (0, 0))

    screen.blit(txt, (10,10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
