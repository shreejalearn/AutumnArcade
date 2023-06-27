import pygame as py
import sys, random
import subprocess

py.init()
clock = py.time.Clock()


font2 = py.font.Font("images/Neucha-Regular.ttf", 50) 
font = py.font.Font("images/Neucha-Regular.ttf", 30)

cookie_image=py.image.load("images/cookie.png")
background = py.image.load("images/bgcookieclicker.jpg")
class Coin:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.radius = 10
        self.color = (255, 215, 0) # gold color
        self.speed = random.randint(2, 5)  

    def draw(self, surface):
        py.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.speed / 2

class Control:
    def __init__(self):
        self.cpc = 1
        self.num_of_cookies = 0
        self.upgrade1_cost = 5
        self.isClicked = False
        self.color = "#9D7E67"

        self.coins = []
        self.last_coin_spawned_time = 0
        self.money=0

        self.circle = py.Rect(400-150,300-150,300,300)
        self.upgradeBtn =  py.Rect(700, 50, 185, 125)
        self.autoClickerBtn = py.Rect(700, 200, 185, 125)
        self.clickMultBtn = py.Rect(700, 350, 185, 125)
        self.chickBtn= py.Rect(900, 50, 185, 125)
        self.catBtn= py.Rect(900, 200, 185, 125)
        self.dogBtn= py.Rect(900, 350, 185, 125)
        self.dragonBtn= py.Rect(1100, 50, 185, 125)
        self.unicornBtn= py.Rect(1100, 200, 185, 125)
        self.auto_clicker_on = False
        self.auto_clicker_cost = 150
        self.auto_clicker_timer = 0
        self.auto_clicker_cps = 1

        self.click_multipliers=1
        self.click_multipliercost=1000

        self.num_autoclicker=0
        self.font = py.font.Font("images/Neucha-Regular.ttf", 25)

    def run(self):
        self.click()
        self.counter()
        self.upgrade()
        self.auto_clicker()
        self.click_multiplier()
        self.pet()
        self.spawn_coin()
        self.update_coins()
        self.show_money()

    def spawn_coin(self):
        current_time = py.time.get_ticks()
        if current_time - self.last_coin_spawned_time >= 3000:  # spawn every 3 seconds
            x = random.randint(50, w-50)
            y = -50
            value = random.randint(1, 5)
            coin = Coin(x, y, value)

            coin.draw(window)
            self.coins.append(coin)
            self.last_coin_spawned_time = current_time


    def update_coins(self):
        for coin in self.coins:
            coin.move()
            coin.draw(window)
            if coin.y >= h-50: # if the coin hits the bottom of the screen
                self.coins.remove(coin)
            elif py.mouse.get_pressed()[0] and py.Rect(coin.x-coin.radius, coin.y-coin.radius, coin.radius*2, coin.radius*2).collidepoint(py.mouse.get_pos()):
                self.money += coin.value
                self.coins.remove(coin)
    def show_money(self):
        font = py.font.SysFont("comicsansms", 20)
        text = font.render("Money: " + str(self.money), True, (0, 0, 0))
        window.blit(text, (10, 50))

        
    def counter(self):
        x=str([self.num_of_cookies])
        self.cookiecount = font2.render("Cookies: "+x, True, "black")
        window.blit(self.cookiecount, (20,500))

    def click(self):
        self.pos = py.mouse.get_pos()
        py.draw.rect(window, self.color, self.circle, border_radius = 150)
        cookie_rect = cookie_image.get_rect(center=(400,300))
        window.blit(cookie_image,cookie_rect)

        if self.upgradeBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0] and self.num_of_cookies>=self.upgrade1_cost:
                self.num_of_cookies-=self.upgrade1_cost
                self.cpc += 1
                self.upgrade1_cost *= 2
                self.cpc += 1

        if self.circle.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.isClicked=True
            else:
                if self.isClicked:
                    self.num_of_cookies +=(self.cpc*self.click_multipliers)
                    self.isClicked=False
                else:
                    pass

        if self.autoClickerBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_auto_clicker()
        if self.clickMultBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_click_multiplier()
        if self.chickBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_chick()
        if self.catBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_cat()
        if self.dogBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_dog()
        if self.dragonBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_unicorn()
        if self.unicornBtn.collidepoint(self.pos):
            if py.mouse.get_pressed()[0]:
                self.buy_dragon()
    def upgrade(self):
        py.draw.rect(window, "#522920", self.upgradeBtn, border_radius=15)
        self.display_cost = font.render(f"Cost: {str(self.upgrade1_cost)}", True, "#eee0b1")
        self.upgrade1_description = self.font.render(f"+{self.cpc} cookie per click", True, "#eee0b1") 

        window.blit(self.upgrade1_description, (715, 65)) 
        window.blit(self.display_cost, (735, 85))

    def auto_clicker(self):
        if not self.auto_clicker_on:
            py.draw.rect(window, "#522920", self.autoClickerBtn, border_radius=15)
            self.auto_clicker_description = self.font.render(f"Buy Autoclicker", True, "#eee0b1")
            self.auto_clicker_c = self.font.render(f"({self.auto_clicker_cost} cookies)", True, "#eee0b1")
            s=self.auto_clicker_cps+1+self.num_autoclicker
            self.auto_clicker_update = self.font.render(f"0 -> {s} cps)", True, "#eee0b1")
            window.blit(self.auto_clicker_description, (725, 215))
            window.blit(self.auto_clicker_c, (725, 245))
            window.blit(self.auto_clicker_update, (725, 275))
            
        else:
            self.auto_clicker_timer += 1
            if self.auto_clicker_timer % 60 == 0:
                self.num_of_cookies += self.auto_clicker_cps
            py.draw.rect(window, "#522920", self.autoClickerBtn, border_radius=15)
            self.auto_clicker_description = self.font.render(f"Buy Autoclicker", True, "#eee0b1")
            self.auto_clicker_c = self.font.render(f"({self.auto_clicker_cost} cookies)", True, "#eee0b1")
            s=self.auto_clicker_cps+1+self.num_autoclicker
            self.auto_clicker_update = self.font.render(f"{int(self.auto_clicker_cps)} -> {s} cps)", True, "#eee0b1")
            window.blit(self.auto_clicker_description, (725, 215))
            window.blit(self.auto_clicker_c, (725, 245))
            window.blit(self.auto_clicker_update, (725, 275))

    def buy_auto_clicker(self):
        if self.num_of_cookies >= self.auto_clicker_cost:
            self.num_of_cookies -= self.auto_clicker_cost
            self.auto_clicker_on = True
            self.auto_clicker_cps+=1+self.num_autoclicker
            self.auto_clicker_cost*=5
            self.num_autoclicker+=1

    def pet(self):
        py.draw.rect(window, "#522920", self.chickBtn, border_radius=15)
        py.draw.rect(window, "#522920", self.catBtn, border_radius=15)
        py.draw.rect(window, "#522920", self.dogBtn, border_radius=15)
        py.draw.rect(window, "#522920", self.unicornBtn, border_radius=15)
        py.draw.rect(window, "#522920", self.dragonBtn, border_radius=15)
        
        chick_text = self.font.render("Buy Chick", True, "#eee0b1")
        chick_cost_text = self.font.render("250 coins, 1 cps", True, "#eee0b1")
        cat_text = self.font.render("Buy Cat", True, "#eee0b1")
        cat_cost_text = self.font.render("1000 coins, 3 cps", True, "#eee0b1")
        dog_text = self.font.render("Buy Dog", True, "#eee0b1")
        dog_cost_text = self.font.render("2500 coins, 5 cps", True, "#eee0b1")
        unicorn_text = self.font.render("Buy Unicorn", True, "#eee0b1")
        unicorn_cost_text = self.font.render("10000 coins, 10 cps", True, "#eee0b1")
        dragon_text = self.font.render("Buy Dragon", True, "#eee0b1")
        dragon_cost_text = self.font.render("25000 coins, 20 cps", True, "#eee0b1")
        instruct_text = self.font.render("Press q to quit", True, "black")

        window.blit(instruct_text, (10,10))
        
        window.blit(chick_text, (905, 75))
        window.blit(chick_cost_text, (905, 100))
        window.blit(cat_text, (910, 225))
        window.blit(cat_cost_text, (905, 250))
        window.blit(dog_text, (920, 375))
        window.blit(dog_cost_text, (905, 400))
        window.blit(unicorn_text, (1110, 75))
        window.blit(unicorn_cost_text, (1105, 100))
        window.blit(dragon_text, (1105, 225))
        window.blit(dragon_cost_text, (1105, 250))
        
    def buy_chick(self):
        if self.num_of_cookies >=250:
            self.num_of_cookies-=250
            self.auto_clicker_on=True
            self.auto_clicker_cps+=1
    def buy_cat(self):
        if self.num_of_cookies >=1000:
            self.num_of_cookies-=1000
            self.auto_clicker_on=True
            self.auto_clicker_cps+=3
    def buy_dog(self):
        if self.num_of_cookies >=2500:
            self.num_of_cookies-=2500
            self.auto_clicker_on=True
            self.auto_clicker_cps+=5
    def buy_unicorn(self):
        if self.num_of_cookies >=10000:
            self.num_of_cookies-=10000
            self.auto_clicker_on=True
            self.auto_clicker_cps+=10
    def buy_dragon(self):
        if self.num_of_cookies >=25000:
            self.num_of_cookies-=25000
            self.auto_clicker_on=True
            self.auto_clicker_cps+=20
    def click_multiplier(self):
        py.draw.rect(window, "#522920", self.clickMultBtn, border_radius=15)
        self.clickmult_description = self.font.render(f"Buy Click Multiplier", True, "#eee0b1")
        self.clickmult_c = self.font.render(f"({self.click_multipliercost} cookies)", True, "#eee0b1")
        self.clickmult_update = self.font.render(f"{float(self.click_multipliers)}x -> {self.click_multipliers+0.25}x)", True, "#eee0b1")
        window.blit(self.clickmult_description, (725, 365))
        window.blit(self.clickmult_c, (725, 395))
        window.blit(self.clickmult_update, (725, 425))

    def buy_click_multiplier(self):
        if self.num_of_cookies >= self.click_multipliercost:
            self.num_of_cookies -= self.click_multipliercost
            self.click_multipliers += 0.25
            self.click_multipliercost *= 2

w, h = 1500, 720
window = py.display.set_mode((w, h))
py.display.set_caption("Cookie Clicker")
background=py.transform.scale(background, (w,h))


running = True
controller = Control()

while running:
    window.blit(background, (0,0))

    controller.run()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
            py.quit()
            sys.exit()
        if event.type==py.KEYDOWN and event.key==py.K_q:
            with open("money.txt") as f:
                contents = f.readlines()
            money=""
            for thing in contents:
                money+=thing
            money=int(money)
            money+=controller.money
            with open('money.txt', 'w') as h:
                h.write(str(money))
            with open("highscores.txt") as z:
                c = z.readlines()
            for g in c:
                x=c.index(g)
                c[x]=g.strip()
            x=(c[5])
            if float(x) < controller.num_of_cookies:
                c[5] = str(controller.num_of_cookies)
            with open('highscores.txt', 'w') as y:
                for t in c:
                    y.write(str(t)+"\n")
            subprocess.Popen("python intro.py")
            py.quit()

    py.display.update()
    clock.tick(60)
