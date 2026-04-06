from pygame import *

win_width = 700
win_height = 500
back =(100, 100,255)
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')
window.fill(back)


class Game_Sprite(sprite.Sprite):
    def __init__(self,picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
 

class Player(Game_Sprite):
    def __init__(self, picture, w,h,x,y, x_speed, y_speed):
        super(). __init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update_ball(self): 
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def update_r(self): 
        keys = key.get_pressed()
        x, y = self.rect.x, self.rect.y 
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.y_speed
        if keys[K_DOWN] and self.rect.y < win_height - 140:
            self.rect.y += self.y_speed

    def update_l(self): 
        keys = key.get_pressed()
        x, y = self.rect.x, self.rect.y 
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.y_speed
        if keys[K_s] and self.rect.y < win_height - 140:
            self.rect.y += self.y_speed
        

    

ball = Player('ball02.png',50, 50 , 200, 200, 5, 5)
player_l = Player('platform_v0.png',30, 140 , 0, 200, 0, 10)	 
player_r = Player('platform_v0.png',30, 140 , 670, 200, 0, 10)	
run = True
finish = False

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.fill(back)
    player_l.reset()
    player_l.update_l()
    player_r.reset()
    player_r.update_r()
    ball.reset()
    ball.update_ball()

    display.update()
