import subprocess
import pygame as py, sys, random


py.init()
clock = py.time.Clock()
screen_width = 800
screen_height = 800
tile = 50
score_font = py.font.Font("images/Neucha-Regular.ttf", tile * 2)
window = py.display.set_mode((screen_width, screen_height))
py.display.set_caption("Snake Game")


global money

money=0
class Food:
    def __init__(self):
        randheight = random.randint(tile, screen_height - tile) // tile
        self.y = int(randheight) * tile

        randwidth = random.randint(tile, screen_width - tile) // tile
        self.x = int(randwidth) * tile

        self.rect = py.Rect(self.x, self.y, tile, tile)

    def draw(self):
        py.draw.rect(window, "orange", self.rect)


class Coin:
    def __init__(self):
        randheight = random.randint(tile, screen_height - tile) // tile
        self.y = int(randheight) * tile

        randwidth = random.randint(tile, screen_width - tile) // tile
        self.x = int(randwidth) * tile

        self.radius = tile // 3
        self.center = (self.x + self.radius, self.y + self.radius)

    def draw(self):
        py.draw.circle(window, "yellow", self.center, self.radius)

c=Coin()

class Snake:
    def __init__(self):
        self.gameOver = False

        self.xdir = 1
        self.x = tile

        self.ydir = 0
        self.y = tile

        self.length = [
            py.Rect(self.x - tile, self.y, tile, tile)
        ]

        self.start = py.Rect(self.x, self.y, tile, tile)

        self.coin = Coin()

    def move(self):
        global food, money
        
        self.coin_rect = py.Rect(
        self.coin.center[0] - self.coin.radius,
        self.coin.center[1] - self.coin.radius,
        self.coin.radius * 2,
        self.coin.radius * 2
        )


        if snake1.start.colliderect(self.coin_rect):
            self.coin = Coin()
            money+=random.randint(1,5)

        self.length.append(self.start)
        l = len(self.length) - 1
        for x in range(l):
            i = self.length[x + 1]
            self.length[x].x = i.x
            self.length[x].y = i.y
        self.start.y += self.ydir * tile
        self.start.x += self.xdir * tile
        self.length.remove(self.start)

        self.coin.draw()

        if self.gameOver:
            with open("highscores.txt") as z:
                c = z.readlines()
            for g in c:
                x=c.index(g)
                c[x]=g.strip()
            x=(c[6])
            if int(x) < len(self.length):
                c[6] = str(len(self.length))
            with open('highscores.txt', 'w') as y:
                for t in c:
                    y.write(str(t)+"\n")
            with open("money.txt") as f:
                contents = f.readlines()
            m=""
            for thing in contents:
                m+=thing
            m=int(m)
            m+=money
            with open('money.txt', 'w') as h:
                h.write(str(m))
            subprocess.Popen("python end_screen.py")
            py.quit()


        for i in self.length:
            if self.start.colliderect(i):
                self.gameOver = True
            if not window.get_rect().colliderect(self.start):
                self.gameOver = True


food = Food()
snake1 = Snake()

start_text = score_font.render("Press space to start", True, "white")
start_rect = start_text.get_rect(center=(screen_width / 2, screen_height / 2))

score = score_font.render("1", True, "white")
score_box = score.get_rect(center=(screen_width / 2, screen_height / 7))

playing = False
while not playing:
    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                playing = True

    window.fill('black')
    start_text = score_font.render("Press space to start", True, "white")
    start_rect = start_text.get_rect(center=(screen_width / 2, screen_height / 2))
    window.blit(start_text, start_rect)
    py.display.update()
    clock.tick(10)

pause = False

while playing:
    if pause!=True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            
            if event.type==py.KEYDOWN:
                if event.key==py.K_p:
                    pause=True


            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    
                    subprocess.Popen("python intro.py")
                    py.quit()


                if event.key == py.K_DOWN and snake1.ydir != -1:
                    snake1.ydir = 1
                    snake1.xdir = 0
                elif event.key == py.K_UP and snake1.ydir != 1:
                    snake1.ydir = -1
                    snake1.xdir = 0
                elif event.key == py.K_RIGHT and snake1.xdir != -1:
                    snake1.ydir = 0
                    snake1.xdir = 1
                elif event.key == py.K_LEFT and snake1.xdir != 1:
                    snake1.ydir = 0
                    snake1.xdir = -1

                if event.key == py.K_s and snake1.ydir != -1:
                    snake1.ydir = 1
                    snake1.xdir = 0
                elif event.key == py.K_w and snake1.ydir != 1:
                    snake1.ydir = -1
                    snake1.xdir = 0
                elif event.key == py.K_d and snake1.xdir != -1:
                    snake1.ydir = 0
                    snake1.xdir = 1
                elif event.key == py.K_a and snake1.xdir != 1:
                    snake1.ydir = 0
                    snake1.xdir = -1

        window.fill('black')

        food.draw()
        snake1.move()

        showscore = score_font.render(f"{len(snake1.length)}", True, "white")
        py.draw.rect(window, "red", snake1.start)
        for unit in snake1.length:
            py.draw.rect(window, "red", unit)
        window.blit(showscore, score_box)

        money_text = score_font.render(f"Money: {money}", True, "white")
        money_box = money_text.get_rect(topleft=(tile, screen_height - tile*3))

        # blit the money surface to the screen
        window.blit(money_text, money_box)

        if snake1.start.colliderect(food.rect):
            snake1.length.append(py.Rect(unit.x, unit.y, tile, tile))
            food = Food()
        
        

        py.display.update()
        clock.tick(10)
    
    else:
        for event in py.event.get():
            if event.type==py.KEYDOWN:
                if event.key==py.K_p:
                    pause=False
