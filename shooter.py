from pygame import *
from random import randint
font.init()
font2 = font.SysFont('Arial', 24)
font1 = font.SysFont('Arial bold', 70)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)


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
       bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


class Ememy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.x = randint(50, 650)  
            self.rect.y = 0      
            lost += 1

class Bullet(GameSprite):
    def update(self):
       self.rect.y += self.speed      
       if self.rect.y < 0:    #исчезает, если дойдет до края экрана
           self.kill()



ship = Player('rocket.png',5, 400, 80, 100, 10)
enemies = sprite.Group()
for i in range(5):
    enemy = Ememy('ufo.png', randint(50, 650), 0, 80, 50, randint(1, 4))
    enemies.add(enemy)
bullets = sprite.Group()
game = True
finish = False
lost = 0
score = 0

win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
while game:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
           game = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
               fire_sound.play()

         
    if not finish:
        window.blit(back,(0,0))
        ship.reset()
        ship.update()  
        enemies.draw(window)
        enemies.update()
	   bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
           score = += 1
           enemy = Enemy('ufo.png', randint(50, 650), 0, 80, 50, randint(1, 4))
           enemies.add(enemy)


        text_lose = font2.render("Пропущено: " + str(lost), True, (255, 255, 255))
        window.blit(text_lose,(10,50))
        text_score = font2.render("Счёт: " + str(score), True, (255, 255, 255))
        window.blit(text_score,(10,20))

        

       #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, enemies, False) or lost > 3:
            finish = True #проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))


        #проверка выигрыша: сколько очков набрали?
        if score > 10:
            finish = True
            window.blit(win, (200, 200))


       #пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        display.update()
   #бонус: автоматический перезапуск игры
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()


        time.delay(3000)
        for i in range(1, 6):
            enemy = Enemy('ufo.png', randint(50, 650), 0, 80, 50, randint(1, 4))
            enemies.add(enemy)
   


    time.delay(50)

