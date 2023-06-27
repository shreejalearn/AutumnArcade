import subprocess, random
import pygame as py

py.init()
font = py.font.SysFont("images/Neucha-Regular.ttf", 90)

w=1000
h = 800
window = py.display.set_mode((w, h))

ball_r = 15

py.display.set_caption("Pong Game")

p_height = 150
p_width=18
global w_score
w_score = 5


class Ball:
    c_gold = (255, 223, 0)
    max_speed = 8
    

    def __init__(self, x, y, r):
        self.x = x
        self.startx = x

        self.xspeed = self.max_speed

        self.yspeed = 0

        self.y = y
        self.starty = y

        self.r = r

    def update(self):
        self.y += self.yspeed
        self.x += self.xspeed

    def restart(self):
        self.x = self.startx
        self.y = self.starty
        self.xspeed *= -1
        self.yspeed = 0
        
    def display(self, win):
        py.draw.circle(win, self.c_gold, (self.x, self.y), self.r)

    def getMaxSpeed(self):
        return self.max_speed


def interact(ball, right_paddle, left_paddle):
    if ball.xspeed >= 0:
        if (right_paddle.y <= ball.y <= right_paddle.y + right_paddle.h and ball.x + ball.r >= right_paddle.x):
            ball.xspeed *= -1.01

            middle_y = right_paddle.y + right_paddle.h / 2
            difference_in_y = middle_y - ball.y
            lower = (right_paddle.h / 2) / ball.max_speed
            y_speed = difference_in_y / lower
            ball.y_speed = -1.01 * y_speed

    if ball.xspeed < 0:
        if (left_paddle.y <= ball.y <= left_paddle.y + left_paddle.h and ball.x - ball.r <= left_paddle.x + left_paddle.w):
            ball.xspeed *= -1.01

            middle_y = left_paddle.y + left_paddle.h / 2
            difference_in_y = middle_y - ball.y
            lower = (left_paddle.h / 2) / ball.max_speed
            y_speed = difference_in_y / lower
            ball.yspeed = -1.01 * y_speed

    if ball.y - ball.r <= 0:
        ball.yspeed *= -1
    if ball.r + ball.y >= h:
        ball.yspeed *= -1
    else:
        pass



def update_display(screen, ball, paddles, rscore, lscore):
    bgcolor =(255,165,0)
    screen.fill(bgcolor)
    
    rtext = font.render(f"{rscore}", 1, (225,225,225))
    ltext = font.render(f"{lscore}", 1, (225,225,225))
    screen.blit(ltext, (w//4 - ltext.get_width()//2, 20))
    screen.blit(rtext, (w * (3/4) -rtext.get_width()//2, 20))


    for x in range(10, h, h // 20):
        if x % 2 == 0:
            py.draw.rect(screen, (255, 255, 255), (w // 2 - 5, x, 10, h // 20))
    
    for i in paddles:
        i.showobj(screen)


    ball.display(screen)
    py.display.update()

class Paddle:
    speed = 8
    c_white = (255, 255, 255)

    def __init__(self, posx, posy, h, w):
        self.x= posx
        self.original_x =posx
        self.y= posy
        self.original_y =posy
        self.h = h
        self.w = w

    def update(self, dirup=True):
        if dirup==False:
            self.y += self.speed
            
        else:
            self.y -= self.speed

    def showobj(self, surface):
        py.draw.rect(
            surface, self.c_white, (self.x, self.y, self.w, self.h))

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

    def getX(self):
        return self.x
    def getY(self):
        self.y
    def getW(self):
        return self.w
    def getH(self):
        return self.h

def p_move(arrow, rp, lp):
    if arrow[py.K_w] and lp.y - lp.speed >= 0:
        lp.update(dirup=True)
    if arrow[py.K_UP] and rp.y - rp.speed >= 0:
        rp.update(dirup=True)
    
    if arrow[py.K_DOWN] and rp.y + rp.speed + rp.h <= h:
        rp.update(dirup=False)
    if arrow[py.K_s] and lp.y + lp.speed + lp.h <= h:
        lp.update(dirup=False)

global won 
global win_text
won = False


def main():
    money=0
    global won, w_score, win_text
    clock = py.time.Clock()
    FPS = 60

    lp = Paddle(10, h//2 - p_height //2, p_height, p_width)
    ball = Ball(w // 2, h // 2, ball_r)
    rp = Paddle(w - 10 - p_width, h //2 - p_height//2, p_height, p_width)

    rscore = 0
    lscore = 0

    go = True
    restart = False 
    paused = False  # add a paused variable

    while go:
        clock.tick(FPS)
        update_display(window, ball, (lp, rp), rscore, lscore)

        for event in py.event.get():
            if event.type == py.QUIT:
                go = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_q:
                    subprocess.Popen("python intro.py")
                    py.quit()
                if event.key == py.K_p:  # check for 'p' key press
                    paused = not paused  # toggle paused variable

        if not paused:  # only update game if not paused
            if ball.x < 0:
                rscore += 1
                ball.restart()
            if ball.x > w:
                lscore += 1
                ball.restart()

            keypress = py.key.get_pressed()
            p_move(keypress, rp, lp)

            ball.update()
            interact(ball, rp, lp)

        if lscore >= w_score:
            won = True
            win_text = "Congrats to Left Player!"
        if rscore >= w_score:
            won = True
            win_text = "Congrats to Right Player!"

        if won:
            window.fill((225, 165, 0)) 
            white = (255, 255, 255)
            text = font.render(win_text, 1, white)
            window.blit(text, (w//2 - text.get_width() //2, h//2 - text.get_height()//2))
            text2 = font.render("Press space to restart, q to quit", 1, white)

            money+=random.randint(2, 6)

            window.blit(text2, (w//2 - text2.get_width() //2, h//2 + text2.get_height()//2))
            text3 = font.render("Money: "+str(money), 1, white)
            window.blit(text3, (350,510))
            py.display.update()

            while True:
                event = py.event.wait()
                if event.type == py.KEYDOWN and event.key == py.K_SPACE:
                    restart = True 
                    break
                if event.type == py.KEYDOWN and event.key == py.K_q:
                    subprocess.Popen("python intro.py")
                    py.quit()

        if restart:
            ball.restart()
            lp.reset()
            rp.reset()
            lscore = 0
            rscore = 0
            won = False  
            restart = False  

    py.quit()

main()
