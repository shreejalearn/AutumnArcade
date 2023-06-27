import pygame
import random
import subprocess

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")


background_image = pygame.image.load("images/space.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
player_image = pygame.image.load("images/spaceship.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (64, 64))
bullet_image = pygame.image.load("images/bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (32, 32))
enemy_image = pygame.image.load("images/invader.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (64, 64))
circle_image = pygame.image.load("images/bullet.png").convert_alpha()
circle_image = pygame.transform.scale(circle_image, (32, 32))

w = 5

global score
score = 0

def restart_game():
    global score, w, play
    score = 0
    w = 5
    play = Control()
    play.run()
    game(w)

class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.radius = 10
        self.color = (255, 215, 0) # gold color
        self.speed = random.randint(2, 5)  

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.speed / 2

class Control:
    def __init__(self):
        self.coins = []
        self.last_coin_spawned_time = 0
        self.money = 0
        self.player_rect = pygame.Rect((screen_width - 64) // 2, screen_height - 64 - 10, 64, 64)
        self.player_radius = 32  # Assuming player's radius is half of its width or height

    def run(self):
        self.spawn_coin()
        self.update_coins()
        self.show_money()

    def spawn_coin(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_coin_spawned_time >= 3000:  # spawn every 3 seconds
            x = random.randint(50, screen_width - 50)
            y = -50
            value = random.randint(1, 5)
            coin = Coin(x, y, value)

            self.coins.append(coin)
            self.last_coin_spawned_time = current_time

    def update_coins(self):
        global player_x, player_y, player_width, player_height 
        for coin in self.coins:
            coin.move()
            if coin.y >= screen_height:  # if the coin hits the bottom of the screen
                self.coins.remove(coin)
            else:
                # Calculate the distance between the center of the coin and the center of the player
                player_center_x = self.player_rect.x + self.player_radius
                player_center_y = self.player_rect.y + self.player_radius 
                coin_center_x = coin.x
                coin_center_y = coin.y
                distance = ((coin_center_x - player_center_x) ** 2 + (coin_center_y - player_center_y) ** 2) ** 0.5

                if distance < self.player_radius + coin.radius:
                    self.money += coin.value
                    self.coins.remove(coin)


    def show_money(self):
        for coin in self.coins:
            coin.draw(screen)

    def update_player_rect(self, x, y, w, h):
        self.player_rect = pygame.Rect(x, y, w, h)


play=Control()
play.run()

global player_width, player_height, player_x, player_y

def game(wave):
    global score
    global bullet_state
    wv=w-4
    player_width = 64
    player_height = 64
    player_x = (screen_width - player_width) // 2
    player_y = screen_height - player_height - 10
    player_speed = 5

    bullet_width = 32
    bullet_height = 32
    bullet_x = 0
    bullet_y = screen_height - player_height - 10
    bullet_speed = 10
    bullet_state = "ready"

    enemy_width = 64
    enemy_height = 64
    enemy_speed = 2

    enemies = []
    enemy_rows = 5
    enemy_cols = 8
    enemy_start_x = 100
    enemy_start_y = 50
    enemy_x_gap = 80
    enemy_y_gap = 70

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            enemy_x = enemy_start_x + enemy_x_gap * col
            enemy_y = enemy_start_y + enemy_y_gap * row
            enemies.append({"x": enemy_x, "y": enemy_y, "speed": enemy_speed, "bullet_state": "ready"})

    circles = []
    circle_speed = 3

    score_font = pygame.font.Font(None, 36)

    running = True
    clock = pygame.time.Clock()

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bullet_image, (x, y))

    def draw_score():
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        wave_text = score_font.render("Wave: " + str(wv), True, (255, 255, 255))
        screen.blit(wave_text, (10, 40))
        money_text = score_font.render("Money: " + str(play.money), True, (255, 255, 255))
        screen.blit(money_text, (10, 70))

    right = False
    left = False  
    pause=False
    pause_font = pygame.font.Font(None, 72)

    while running:
        if pause!=True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    subprocess.Popen("python end_screen.py")

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_p:
                        pause=True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and player_x > 0:
                        left = True
                    if event.key == pygame.K_RIGHT and player_x < screen_width - player_width:
                        right = True
                    if event.key == pygame.K_SPACE and bullet_state == "ready":
                        bullet_x = player_x + player_width // 2 - bullet_width // 2
                        bullet_y = player_y
                        fire_bullet(bullet_x, bullet_y)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    if event.key == pygame.K_RIGHT:
                        right = False
            if pause:
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
                screen.blit(pause_text, (screen_width // 2 - 100, screen_height // 2))

            else:

                if right and player_x < screen_width - player_width:
                    player_x += player_speed
                if left and player_x > 0:
                    player_x -= player_speed

                screen.blit(background_image, (0, 0))

                if bullet_state == "fire":
                    bullet_y -= bullet_speed
                    if bullet_y < 0:
                        bullet_state = "ready"

                for enemy in enemies:
                    enemy_x = enemy["x"]
                    enemy_y = enemy["y"]

                    enemy_x += enemy["speed"]
                    if enemy_x <= 0 or enemy_x >= screen_width - enemy_width:
                        for e in enemies:
                            e["speed"] *= -1
                            e["y"] += wave
                        enemy_y += wave

                    enemy["x"] = enemy_x
                    enemy["y"] = enemy_y

                    if (
                        bullet_x < enemy_x + enemy_width
                        and bullet_x + bullet_width > enemy_x
                        and bullet_y < enemy_y + enemy_height
                        and bullet_y + bullet_height > enemy_y
                    ):
                        bullet_state = "ready"
                        enemies.remove(enemy)
                        score += 1

                    if (
                        player_x < enemy_x + enemy_width
                        and player_x + player_width > enemy_x
                        and player_y < enemy_y + enemy_height
                        and player_y + player_height > enemy_y
                    ):
                        subprocess.Popen("python end_screen.py")
                        pygame.quit()

                    screen.blit(enemy_image, (enemy_x, enemy_y))

                if bullet_state == "fire":
                    screen.blit(bullet_image, (bullet_x, bullet_y))
                    bullet_y -= bullet_speed

                for circle in circles:
                    circle_x = circle["x"]
                    circle_y = circle["y"]

                    circle_y += circle_speed

                    if (
                        player_x < circle_x + bullet_width
                        and player_x + player_width > circle_x
                        and player_y < circle_y + bullet_height
                        and player_y + player_height > circle_y
                    ):

                        with open("money.txt") as f:
                            contents = f.readlines()
                        money=""
                        for thing in contents:
                            money+=thing
                        money=int(money)
                        money+=play.money

                        with open('money.txt', 'w') as h:
                            h.write(str(money))
                        with open("highscores.txt") as z:
                            c = z.readlines()
                        for g in c:
                            x=c.index(g)
                            c[x]=g.strip()
                        x=(c[2])
                        if int(x) < score:
                            c[2] = str(score)
                        with open('highscores.txt', 'w') as y:
                            for t in c:
                                y.write(str(t)+"\n")
                        subprocess.Popen("python end_screen.py")
                        pygame.quit()

                    if circle_y > screen_height:
                        circles.remove(circle)

                    screen.blit(circle_image, (circle_x, circle_y))

                if random.randint(0, 500) < wave:
                    r=random.randint(0,len(enemies)-1)

                    circle_x = (enemies[r])["x"]
                    circle_y = (enemies[r])["y"]
                    circles.append({"x": circle_x, "y": circle_y})

                for circle in circles:
                    circle["y"]+=1 

                screen.blit(player_image, (player_x, player_y))
                draw_score()

                if len(enemies) == 0:
                    break
                play.update_player_rect(player_x, player_y, player_width, player_height)
                play.run()

                pygame.display.update()
                clock.tick(60)
        
        else:
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_p:
                        pause=False


while True:
    game(w)
    w += 1