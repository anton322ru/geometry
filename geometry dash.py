import pygame
import os
import sys
import random

pygame.init()
size = w, h = (800, 400)
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as mes:
        print(f'Не могу загрузить файл: {name}')
        print(mes)
        return
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (100, h - 50)
        self.y = 0
        self.on_ground = True

    def update(self):
        self.y += 1
        self.rect.y += self.y
        if self.rect.bottom >= h - 50:
            self.rect.bottom = h - 50
            self.on_ground = True
            self.y = 0

    def jump(self):
        if self.on_ground:
            self.y = -10
            self.on_ground = False

class Treug(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('treug.png')
        self.rect = self.image.get_rect()
        self.rect.center = (w + 100, h - 50)
        self.speed = -10

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
treugs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

def spawn_treug():
    treug = Treug()
    all_sprites.add(treug)
    treugs.add(treug)

running = True
spawn_delay = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    spawn_delay += 1
    if spawn_delay >= 120:
        spawn_treug()
        spawn_delay = 0
    all_sprites.update()
    if pygame.sprite.spritecollideany(player, treugs):
        running = False

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()