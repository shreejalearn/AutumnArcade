import random; import pygame as py; from pygame.locals import *
import subprocess

clock = py.time.Clock()

sh = 700
sw = 550
run = False

path = (100, 0, 300, sh) #road

win = (sw, sh)

py.init()
py.display.set_caption('Zoom Zoom')
display = py.display.set_mode(win)

othercars = [py.image.load(f'images/{f}') for f in ['car2.png', 'car3.png', 'car4.png', 'car5.png']]
death = py.image.load('images/dead.png')

coin_image = py.image.load('images/coin.png')

scroll_lane = 0 #scrolling bg
sprite_init = py.sprite.Sprite

class Setup(sprite_init):
    def __init__(self, image, x, y):
        self.image = py.transform.smoothscale(image, (70, 70))
        self.rect = self.image.get_rect(center=(x, y))
        super().__init__()
class Coin(Setup):
    def __init__(self, x, y):
        super().__init__(coin_image, x, y)
    
score = 0
money=0
starty = 650
startx = 250 

class PlayerVehicle(Setup):
    def __init__(self, x, y):
        pic = py.image.load('images/car1.png')
        super().__init__(pic, x, y)
      


player = PlayerVehicle(startx, starty)
players = py.sprite.Group()
players.add(player)

lane_coordinates = [150, 250, 350]

dividerh = 40 #white lines of lane
dividerw = 9 #white lines of lane

edge_r = (395, 0, dividerh, sh) #right edge
edge_l = (95, 0, dividerw, sh) #left edge

speed=2.1

running = True
enemy = py.sprite.Group()
coins = py.sprite.Group()
global pause
pause=False
showdeath = death.get_rect()

def paused():
    global pause, run
    while pause == True:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                quit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_p:
                    pause = False
                    break
                if event.key == py.K_q:
                    with open("money.txt") as f:
                        contents = f.readlines()
                    m=""
                    for thing in contents:
                        m+=thing
                    m=int(m)
                    m+=money

                    with open('money.txt', 'w') as h:
                        h.write(str(m))
                    subprocess.Popen("python intro.py")
                    py.quit()
                if event.key == py.K_r:
                    with open("money.txt") as f:
                        contents = f.readlines()
                    m=""
                    for thing in contents:
                        m+=thing
                    m=int(m)
                    m+=money

                    with open('money.txt', 'w') as h:
                        h.write(str(m))
                    subprocess.Popen("python race.py")
                    py.quit()
        display.fill(("#AA4A44")) #grass
            
        #edges
        py.draw.rect(display, ("#ffa500"), edge_r)
        py.draw.rect(display, ("#ffa500"), edge_l)

        py.draw.rect(display, (100, 100, 100), path) #road
        for y in range(-dividerh*2, sh, dividerh*2):
            for x in (lane_coordinates[0]+45, lane_coordinates[1]+45):
                py.draw.rect(display, (255,255,255), (x, y+scroll_lane, dividerw, dividerh))
        players.draw(display)
        enemy.draw(display)
        coins.draw(display)
        display.blit(show, div)
        display.blit(show1, div1)
        display.blit(show2, div2)
        display.blit(show3, div3)
        display.blit(show_coins, (10,150))
        py.display.update()
        clock.tick(15)

while running==True:
    if pause!=True:
        display.fill(("#AA4A44")) #grass
            
        #edges
        py.draw.rect(display, ("#ffa500"), edge_r)
        py.draw.rect(display, ("#ffa500"), edge_l)

        py.draw.rect(display, (100, 100, 100), path) #road

        clock.tick(120)
        
        for i in py.event.get():            
            if i.type == KEYDOWN:
                
                if i.key == K_RIGHT:
                    if player.rect.center[0] < lane_coordinates[2]:
                        player.rect.x += 100

                if i.key == K_LEFT:
                    if player.rect.center[0] > lane_coordinates[0]:
                        player.rect.x -= 100
                if i.key == py.K_p:
                    pause=True
                    paused()
                if i.key == py.K_q:
                    with open("money.txt") as f:
                        contents = f.readlines()
                    m=""
                    for thing in contents:
                        m+=thing
                    m=int(m)
                    m+=money

                    with open('money.txt', 'w') as h:
                        h.write(str(m))
                    subprocess.Popen("python intro.py")
                    py.quit()
                if i.key == py.K_r:
                    with open("money.txt") as f:
                        contents = f.readlines()
                    m=""
                    for thing in contents:
                        m+=thing
                    m=int(m)
                    m+=money

                    with open('money.txt', 'w') as h:
                        h.write(str(m))
                    subprocess.Popen("python race.py")
                    py.quit()
                    
                for car in enemy: # collision after lane switch
                    if py.sprite.collide_rect(player, car):
                        
                        run = True
                        
                        if i.key == K_RIGHT:
                            player.rect.right = car.rect.left
                            showdeath.center = [
                                player.rect.right,
                                (player.rect.center[1] + car.rect.center[1]) / 2
                            ]
                        
                        if i.key == K_LEFT:
                            player.rect.left = car.rect.right
                            showdeath.center = [
                                player.rect.left,
                                (player.rect.center[1] + car.rect.center[1]) / 2
                            ]
                    for coin in coins:
                        if py.sprite.collide_rect(car,coin):
                            coin.kill() 
                    

                
                        
            if i.type == QUIT:
                running = False
            

        if scroll_lane >= dividerh * 2:
            scroll_lane = 0

        for y in range(-dividerh*2, sh, dividerh*2):
            for x in (lane_coordinates[0]+45, lane_coordinates[1]+45):
                py.draw.rect(display, (255,255,255), (x, y+scroll_lane, dividerw, dividerh))
        for coin in coins:
            if py.sprite.collide_rect(player,coin):
                money+=random.randint(1,3)
                coin.kill() 
        scroll_lane = scroll_lane+speed * 2  
        
        f1 = py.font.Font("images/Neucha-Regular.ttf", 24)
        show = f1.render('Score: ' + str(score), True, (255, 255, 255))
        show1 = f1.render(('r=restart'), True, (255, 255, 255))
        show2 = f1.render(('p=pause'), True, (255, 255, 255))
        show3 = f1.render(('q=quit'), True, (255, 255, 255))
        show_coins = f1.render('Money: ' + str(money), True, (255, 255, 255))
        
        if len(enemy) < 3:
            
            new = True #enough gap between vehicles
            for z in enemy:
                if z.rect.top < z.rect.height * 1.5:
                    new = False
                    
            if new==True:
                pic = random.choice(othercars)
                l = random.choice(lane_coordinates)
                car = Setup(pic, l, sh / -2)
                enemy.add(car)

        if len(coins) < 1:
            new = True #enough gap between coins
            for z in coins:
                if z.rect.top < z.rect.height * 2.5:
                    new = False
            if new == True:
                l = random.choice(lane_coordinates)
                coin = Coin(l, sh / -2)
                coins.add(coin)
            
        players.draw(display)
        enemy.draw(display)
        coins.draw(display)


        for t in enemy:
            t.rect.y = t.rect.y+speed
            
            if t.rect.top >= sh:
                t.kill()

                score += 1

                if score % 8 == 0:
                    speed += 0.5
        for coin in coins:
            coin.rect.y=coin.rect.y+speed
            if coin.rect.top>=sh:
                coin.kill()
        
        div = show.get_rect()
        div.center = (44, 100)

        div1 = show1.get_rect()
        div1.center = (44, 200)

        div2 = show2.get_rect()
        div2.center = (44, 250)

        div3 = show3.get_rect()
        div3.center = (44, 300)

        
        
        if py.sprite.spritecollide(player, enemy, True):
            run = True
            showdeath.center = [player.rect.centerx, player.rect.top]
                
        if run:
            with open("highscores.txt") as z:
                c = z.readlines()
            for g in c:
                x=c.index(g)
                c[x]=g.strip()
            x=(c[7])
            if int(x) < score:
                c[7] = str(score)
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

        for car in enemy: # collision after lane switch
            if py.sprite.collide_rect(player, car):
                        
                run = True
                        
                if i.key == K_RIGHT:
                    player.rect.right = car.rect.left
                    showdeath.center = [
                        player.rect.right,
                        (player.rect.center[1] + car.rect.center[1]) / 2
                    ]
                        
                if i.key == K_LEFT:
                    player.rect.left = car.rect.right
                    showdeath.center = [
                        player.rect.left,
                        (player.rect.center[1] + car.rect.center[1]) / 2
                    ]
            for coin in coins:
                if py.sprite.collide_rect(car,coin):
                    coin.kill() 
        
        display.blit(show, div)
        display.blit(show1, div1)
        display.blit(show2, div2)
        display.blit(show3, div3)
        display.blit(show_coins, (10,150))
        
                
        py.display.update()
with open("money.txt") as f:
    contents = f.readlines()
m=""
for thing in contents:
    m+=thing
m=int(m)
m+=money

with open('money.txt', 'w') as h:
    h.write(str(m))
subprocess.Popen("python intro.py")
py.quit()