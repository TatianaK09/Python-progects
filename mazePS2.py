#PS-2 
from pygame import *

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))


class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x = 65, size_y = 65, player_speed=5):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):#пули
       
   
    def update(self):
        self.rect.x += self.speed
        # исчезает, если дойдёт до края экрана
        if self.rect.x > win_width+10:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        x, y = self.rect.x, self.rect.y #исходные координаты игрока
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if sprite.spritecollide(self, walls, False):
            self.rect.x = 5
            self.rect.y = 420  #возвращается в исходную точку
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if sprite.spritecollide(self, walls, False): #столкновение со стенами
            self.rect.x = 5
            self.rect.y = 420

       

    def fire(self): #пули
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 10, 5)
        bullets.add(bullet)
        print(5555)

class Enemy(GameSprite):
    direction = "left"
    def update(self, x_left = 0, x_right = 700):
        if self.rect.x <= x_left:
            self.direction = "right"
        if self.rect.x >= x_right:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color, w, h, x, y):
        super().__init__()
        self.image = Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



#стены
wall_1 = Wall((0,50,30), 15, 400, 80, 70)
wall_2 = Wall((0,50,30), 70, 15, 80, 300)
wall_3 = Wall((0,50,30), 15, 300, 250, 100)
wall_4 = Wall((0,50,30), 15, 400, 400, 70)
wall_5 = Wall((0,50,30), 250, 15, 350, 200)


#Персонажи игры:
player = Player('hero.png', 5, 420, player_speed= 4)
monster = Enemy('cyborg.png', 620, 380, player_speed=2)
monster2 = Enemy('cyborg.png', 120, 40, player_speed=2)
final = GameSprite('treasure.png', 420, 420,player_speed=0)

walls = sprite.Group()
walls.add(wall_1)
walls.add(wall_2)
walls.add(wall_3)
walls.add(wall_4)
walls.add(wall_5)
enemes = sprite.Group()
enemes.add(monster)
enemes.add(monster2)
bullets = sprite.Group()


game = True
clock = time.Clock()
FPS = 60


#музыка
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

finish = False
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (255, 105, 0))
restart = font.render('Press RETURN for RESTART', True, (255, 215, 0))

while game:
   
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if finish != True:
        window.blit(background,(0, 0))
        player.reset()
        player.update()
        monster.reset()
        monster.update(450, 600)
        monster2.reset()
        monster2.update(100, 300)
        final.reset()
        #wall_1.reset()
        #wall_2.reset()
        #wall_3.reset()
        #wall_4.reset()
        #wall_5.reset()
        bullets.update()#пули
        bullets.draw(window)#
        #walls.update()
        walls.draw(window)


        sprite.groupcollide(enemes, bullets, True, True)
        sprite.groupcollide(bullets, walls, True, False)


        if sprite.collide_rect(player, final):
            window.blit(win, (200,200))
            finish = True            
            money.play()
        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, monster2):# or sprite.collide_rect(player, wall_1) or sprite.collide_rect(player, wall_2) or sprite.collide_rect(player, wall_3) or sprite.collide_rect(player, wall_4) or sprite.collide_rect(player, wall_5):
            window.blit(lose, (200,200))
            finish = True
            kick.play()
    if finish == True:
        window.blit(restart, (70,300))
        keys = key.get_pressed()
        if keys[K_RETURN]:        
            finish = False
            player.rect.x = 5
            player.rect.y = 420
            mixer.music.play(-1)

   

    display.update()
    clock.tick(FPS)
