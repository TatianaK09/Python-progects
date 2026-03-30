from pygame import *

window = display.set_mode((700,500))
display.set_caption('Лабиринт')


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

    def update(self): 
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

	    if self.rect.x >= 700-70 or self.rect.x < 0:
            self.x_speed = 0
        if self.rect.y >= 500-70 or self.rect.y < 0:
            self.y_speed = 0

        if sprite.spritecollide(self, walls, False): #столкновение со стенами
            self.rect.x = 50
            self.rect.y = 400


               
       

   
   
    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(Game_Sprite):
    side = 'left'
    def __init__(self, picture, w,h,x,y, x_speed, y_speed):
        super(). __init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        if self.rect.x <= 250:
            self.side = 'right'
        if self.rect.x >= 600:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.x_speed
        if self.side == 'right':
            self.rect.x += self.x_speed

class Bullet(Game_Sprite):
    def __init__(self, picture, w,h,x,y, speed):
        super(). __init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= 720:
            self.kill()


wall_v = Game_Sprite('platform_v.png', 30, 300, 200, 100)
wall_h = Game_Sprite('platform_h.png', 180,30, 200,200)
player = Player('hero.png', 80, 80, 5, 400, 0, 0)
enemy_1 = Enemy('cyborg.png', 80,80, 200, 50, 5,5)
enemy_2 = Enemy('cyborg.png', 80,80, 400, 400, 5,5)
packman = Game_Sprite('pac-1.png', 80,80, 0, 0)
walls = sprite.Group()
bullets = sprite.Group()
walls.add(wall_h)
walls.add(wall_v)
enemes = sprite.Group()
enemes.add(enemy_1)
enemes.add(enemy_2)


run = True
finish = False

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed =-5
            elif e.key == K_DOWN:
                player.y_speed =5
            elif e.key == K_LEFT:
                player.x_speed =-5
            elif e.key == K_RIGHT:
                player.x_speed =5
            elif e.key == K_SPACE:  #пули
                player.fire()
           
        elif e.type == KEYUP:  
            if e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_LEFT:
                player.x_speed =0
            elif e.key == K_DOWN:
                player.y_speed =0
            elif e.key == K_RIGHT:
                player.x_speed =0

   
    if not finish:    
        window.fill((0,175,175))
        wall_v.reset()
        wall_h.reset()
        player.reset()
        player.update()
        enemes.draw(window)
        #enemy_1.reset()
        enemy_1.update()
        #enemy_2.reset()
        enemy_2.update()
        packman.reset()
        walls.draw(window)
        bullets.update()
        bullets.draw(window)
        sprite.groupcollide(enemes, bullets, True, True)
        sprite.groupcollide(bullets, walls, True, False)
        if sprite.spritecollide(player, enemes, False):
            finish = True
            img = image.load('game_over.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (700, 500)), (0, 0))
        if sprite.collide_rect(player ,packman):
            finish = True
            img = image.load('you_win.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (700,500)), (0, 0))


    display.update()
