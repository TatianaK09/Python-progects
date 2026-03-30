from pygame import *
from random import randint
from time import time as timer
font.init()
font2 = font.SysFont('Arial bold', 24)
font1 = font.SysFont('Arial bold', 70)

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()
window = display.set_mode((700,500))
display.set_caption('Shooter')
back = transform.scale(image.load('galaxy.jpg'),(700,500))
class GameSprite(sprite.Sprite):

    def __init__(self, img_path, x, y, w, h, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(img_path), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):  
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
   
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(50, 650)  
            self.rect.y = -50  
            lost += 1  

class Bullet(GameSprite):  
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player('rocket.png',5, 400, 80, 100, 5)
enemies = sprite.Group()
for i in range(6):
    enemy = Enemy('ufo.png', randint(0, 620), -50, 80, 50, randint(1, 5))
    enemies.add(enemy)
asteroids = sprite.Group()
asteroid = Enemy('asteroid.png', randint(0, 620), -50, 80, 80, randint(5,7))
asteroids.add(asteroid)
stars = sprite.Group()
star = Enemy('star.png', randint(0, 620), -50, 80, 80, randint(5, 9))
stars.add(star)
bullets = sprite.Group()
game = True
finish = False
rel_time = False
num_fire =0
lost = 0
score = 0
life = 5
win = font1.render('YOU WIN!', True, (0, 180, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

while game:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
           game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                       num_fire += 1
                       fire_sound.play()
                       ship.fire()
                     
                if num_fire  >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
         
    if not finish:
        window.blit(back,(0,0))
        ship.reset()
        ship.update()
        enemies.draw(window)
        enemies.update()
        text_lose = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose,(10,50))
        text_score = font2.render("Счёт: " + str(score), True, (255, 255, 255))
        window.blit(text_score,(10,20))
        text_life = font1.render(str(life), True, (0, 255, 0))
        window.blit(text_life,(650,10))
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        stars.draw(window)
        stars.update()
        if rel_time == True:
           new_time = timer()
       
           if new_time - last_time < 3:
               reload = font1.render('Wait, reload...', True, (150, 0, 0))
               window.blit(reload, (260, 460))
           else:
               num_fire = 0  
               rel_time = False


        if sprite.spritecollide(ship, enemies, True):
            life -= 1
            enemy = Enemy('ufo.png', randint(0, 620), -50, 80, 50, randint(1, 5))
            enemies.add(enemy)
        if sprite.spritecollide(ship, asteroids, True):
            life -= 2
            asteroid = Enemy('asteroid.png', randint(0, 620), -50, 80, 80, randint(5,7))
            asteroids.add(asteroid)
        if sprite.spritecollide(ship, stars, True):
            life += 1
            star = Enemy('star.png', randint(0, 620), -50, 80, 80, randint(5, 9))
            stars.add(star)

        text_life = font1.render(str(life), True, (0, 255, 0))
        window.blit(text_life,(650,10))
       
        if life == 0 or lost >= 10:
            window.blit(lose, (200, 200))
            finish = True
       
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for collide in collides:
            score += 1
            text_score = font2.render("Счёт: " + str(score), True, (255, 255, 255))
            window.blit(text_score,(10,20))
            enemy = Enemy('ufo.png', randint(0, 620), -50, 80, 50, randint(1, 7))
            enemies.add(enemy)
        if score >= 10:
            window.blit(text_score,(10,20))
            window.blit(win, (200, 200))
            finish = True

        display.update()
    time.delay(50)



