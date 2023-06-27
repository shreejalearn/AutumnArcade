import pygame
import math
import random
import os
import subprocess

pygame.init()
clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 600
GRAVITY = 0.8
JUMP_FORCE = -15
DASH_MAX = 100
DASH_REGEN_RATE = 0.2
DASH_CONSUME_RATE = 1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner Game")
bg = pygame.image.load("images/scrollerbackground.png").convert_alpha()
bg=pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_width = bg.get_width()
bg_rect = bg.get_rect()
score = 0

obs1 = [pygame.image.load("images/pipe_bottom.png").convert_alpha(), 50, 200]
obs2 = [pygame.image.load("images/pipe_top.png").convert_alpha(), 50, 200]

pausebutton = pygame.transform.scale(pygame.image.load("images/pause.png"), (150, 150))

obslist = [obs1, obs2]

scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
indexon = 0
megacount = 0
jumpon = 0
jumpcount = 0
r = False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_type):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        thing = obslist[obstacle_type]
        self.image = pygame.transform.scale(thing[0], ((50, y)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        if obstacle_type == 0:
            self.rect.y = SCREEN_HEIGHT - y
        elif obstacle_type == 1:
            self.rect.y = 0

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.f1 = pygame.transform.scale(pygame.image.load("images/bird_down.png"), (48, 48))
        self.f2 = pygame.transform.scale(pygame.image.load("images/bird_mid.png"), (48, 48))
        self.f3 = pygame.transform.scale(pygame.image.load("images/bird_up.png"), (48, 48))
        self.animlist=[self.f1,self.f2,self.f3]

        self.image = self.animlist[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.dash = DASH_MAX
        self.money =0

    def update(self):
        global run
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - 65:
            run = False
        if self.rect.y <= 0:
            run = False
        self.dash += DASH_REGEN_RATE
        if self.dash > DASH_MAX:
            self.dash = DASH_MAX

        die = pygame.sprite.spritecollide(self, obstacle_group, False)
        if die:
            run = False
        self.image = self.animlist[indexon]

obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

global run
run = True
freq = 250
counter = 0
coin_counter = 0
coin_freq = 400
global pause
pause = False

scrollmin = 5

player = Player(50, SCREEN_HEIGHT/2)
player_group = pygame.sprite.Group()
player_group.add(player)

def paused():
    global pause, run
    while pause == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                if event.key == pygame.K_q:
                    run = False
                    pause = False
        dash_bar_width = player.dash / DASH_MAX * 100
        pygame.draw.rect(screen, (0, 0, 0), (10, 50, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (10, 50, dash_bar_width, 10))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        money_text = font.render(f"Money: {player.money}", True, (0, 0, 0))
        screen.blit(money_text, (10, 70))

        pause_text = font.render("Press 'P' to unpause", True, (0, 0, 0))
        screen.blit(pause_text, (SCREEN_WIDTH-250, 10))

        pygame.display.update()
        clock.tick(15)

dash_bar_width = player.dash / DASH_MAX * 100

while run:
    if pause != True:
        megacount += 1
        if(megacount%5==0):
            indexon+=1
            score+=1
            if indexon==3:
                indexon=0
        if (megacount%25==0):
            freq-=1
            if freq==50:
                freq=50

        clock.tick(FPS)

        for i in range(0, tiles):
            screen.blit(bg, (i * bg_width + scroll, 0))
            bg_rect.x = i * bg_width + scroll
        counter += 1
        if counter >= freq:
            obstacle_type = random.randint(0, 2)
            if obstacle_type!=2:
                new_obstacle = Obstacle(SCREEN_WIDTH, random.randint(200, 350), obstacle_type)
                obstacle_group.add(new_obstacle)
            else:
                new_obstacle = Obstacle(SCREEN_WIDTH, random.randint(100, 150), 0)
                obstacle_group.add(new_obstacle)
                new_obstacle = Obstacle(SCREEN_WIDTH, random.randint(100, 150), 1)
                obstacle_group.add(new_obstacle)
            counter = 0

        coin_counter += 1
        if coin_counter >= coin_freq:
            new_coin = Coin(SCREEN_WIDTH, random.randint(100, SCREEN_HEIGHT - 100))
            coin_group.add(new_coin)
            coin_counter = 0

        last_obstacle_passed = None
        for obstacle in obstacle_group:
            obstacle.rect.x -= scrollmin
            if player.rect.colliderect(obstacle.rect) and obstacle.rect.right < player.rect.left:
                last_obstacle_passed = obstacle

        for coin in coin_group:
            coin.rect.x -= scrollmin
            if player.rect.colliderect(coin.rect):
                coin_group.remove(coin)
                player.money+=1

        obstacle_group.draw(screen)
        coin_group.draw(screen)
        player_group.update()
        player_group.draw(screen)
        scroll -= scrollmin

        die = pygame.sprite.spritecollide(player, obstacle_group, False)
        if die:
            run = False
        if abs(scroll) > bg_width:
            scroll = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.velocity_y = JUMP_FORCE
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_RIGHT:
                    r = True
                    oldfreq=freq

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    r = False
                    scrollmin = 5
                    freq = oldfreq


            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()

        if r==True:
            if player.dash >=DASH_CONSUME_RATE:
                player.dash-=DASH_CONSUME_RATE
                dash_bar_width = player.dash / DASH_MAX * 100
                scrollmin=10
                freq=oldfreq-100
            else:
                scrollmin=5
                freq=oldfreq


        dash_bar_width = player.dash / DASH_MAX * 100
        pygame.draw.rect(screen, (0, 0, 0), (10, 50, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (10, 50, dash_bar_width, 10))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (225, 225, 225))
        screen.blit(score_text, (10, 10))

        money_text = font.render(f"Money: {player.money}", True, (225, 225, 225))
        screen.blit(money_text, (10, 70))

        pause_text = font.render("Press 'P' to pause", True, (225, 225, 225))
        screen.blit(pause_text, (SCREEN_WIDTH-250, 10))

        pygame.display.update()

with open("money.txt") as f:
    contents = f.readlines()
money=""
for thing in contents:
    money+=thing
money=int(money)
money+=player.money

with open('money.txt', 'w') as h:
    h.write(str(money))

with open("highscores.txt") as z:
    c = z.readlines()
for g in c:
    x=c.index(g)
    c[x]=g.strip()
x=(c[4])
if int(x) < score:
    c[4] = str(score)
with open('highscores.txt', 'w') as y:
    for t in c:
        y.write(str(t)+"\n")

subprocess.Popen("python end_screen.py")
pygame.quit()
