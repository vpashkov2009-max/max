#Создай собственный Шутер!

from pygame import *
mixer.init()
font.init()
from random import randint
#музыка
mixer.music.load('Bullets_For_My_Valentine_-_Tears_Dont_Fall_(SkySound.cc).mp3')
mixer music.play()
#окно
win = display.set_mode((700, 500))
game = True
#переменные
finish = False
fps = 60
text1 = font.Font(None, 30)
text2 = font.Font(None, 30)
text3 = font.Font(None, 70)
text4 = font.Font(None, 70)
number = 0
method_skipa = 0
#фон
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
#музыка
mixer.music.load('space.ogg')
#таймер
clock = time.Clock()
global bullet_group
bullet_group = sprite.Group()
#класс для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, image1, x_hero, y_hero, speed_hero, size_1, size_2):
        super().__init__()
        self.image = transform.scale(image.load(image1), (size_1, size_2))
        self.speed_hero = speed_hero
        self.rect = self.image.get_rect()
        self.rect.x = x_hero
        self.rect.y = y_hero
        self.size1 = size_1
        self.size2 = size_2
    def blit(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
#класс для передвижения спрайта player
class Player(GameSprite):
    def __init__(self, image1, x_hero, y_hero, speed_hero, size_1, size_2):
        super().__init__(image1, x_hero, y_hero, speed_hero, size_1, size_2)
    def update(self):
        down = key.get_pressed()
        if down[K_d] and self.rect.x < 600:
            self.rect.x += self.speed_hero
        if down[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed_hero
    def fire(self):
        global bullet_group
        bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 15, 20, 20)
        bullet_group.add(bullet)
#класс enemy
class Enemy(GameSprite):
    def __init__(self, image1, x_hero, y_hero, speed_hero, size_1, size_2):
        super().__init__(image1, x_hero, y_hero, speed_hero, size_1, size_2)
    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed_hero
        global method_skipa
        if self.rect.y >= 500:
            self.rect.x = randint(0, 600)
            method_skipa = method_skipa + 1
            self.rect.y = 0
#класс bullet
class Bullet(GameSprite):
    def __init__(self, image1, x_hero, y_hero, speed_hero, size_1, size_2):
        super().__init__(image1, x_hero, y_hero, speed_hero, size_1, size_2)
    def update(self):
        self.rect.y -= self.speed_hero
        if self.rect.y < - 10:
            self.kill()
#летающие тарелки enemy
enemy1 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
enemy2 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
enemy3 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
enemy4 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
enemy5 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
enemy6 = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
#группа тарелок 
enemy_sprite = sprite.Group()
enemy_sprite.add(enemy1)
enemy_sprite.add(enemy2)
enemy_sprite.add(enemy3)
enemy_sprite.add(enemy4)
enemy_sprite.add(enemy5)
enemy_sprite.add(enemy6)
#группа пуль
#спрайт player
player1 = Player('rocket.png', 350, 400, 10, 110, 110)
#цикл
point = 0
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
    win.blit(background, (0,0))
    player1.blit()
    if finish != True:
        press = key.get_pressed()
        player1.update()
        enemy_sprite.draw(win)
        enemy_sprite.update()
        text_skip = text2.render('Пропущено:' + str(method_skipa), True, (255, 255, 255))
        win.blit(text_skip, (50, 50))
        if method_skipa >= 3 or sprite.spritecollide(player1, enemy_sprite, False):
            finish = True
            youlose = text4.render('YOU LOSE!!', True, (255, 0, 0))
            win.blit(youlose, (200, 300))
        if press[K_SPACE]:
            player1.fire()
        sprites_list = sprite.groupcollide(enemy_sprite, bullet_group, True, True)
        for i in sprites_list:
            enemy = Enemy('ufo.png', randint(80, 600), 0, randint(1, 3), 90, 70)
            enemy_sprite.add(enemy)
            point += 1
            if point == 10 or point > 10:
                finish = True
                youwin = text3.render('YOU WIN!!', True, (0, 255, 0))
                win.blit(youwin, (200, 300))
        bullet_group.draw(win)
        bullet_group.update()

    clock.tick(fps)
    display.update()
