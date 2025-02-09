import os
import sys

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as mes:
        print(f'Не могу загрузить файл: {name}')
        return
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '^':
                Treug(x, y)
            elif level[y][x] == '=':
                FloorBlock(x, y)
            elif level[y][x] == '$':
                Coin(x, y)
    return new_player


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height
        self.gravita = 0
        self.on_ground = False

    def update(self):
        self.gravita += 0.7
        self.rect.y += self.gravita

        if pygame.sprite.spritecollideany(self, floor_blocks):
            self.on_ground = True
            self.gravita = 0
            self.rect.bottom = pygame.sprite.spritecollide(self, floor_blocks, False)[0].rect.top
        else:
            self.on_ground = False

        if self.rect.left > w:
            global running
            running = False

    def jump(self):
        if self.on_ground:
            self.gravita = -15
            self.on_ground = False


class Treug(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(treugs, all_sprites)
        self.image = load_image('treug.png', color_key=-1)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height

    def update(self):
        self.rect.x -= 5  # я скорость x
        if self.rect.right < 0:
            self.kill()


class FloorBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(floor_blocks, all_sprites)
        self.image = load_image('floor.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height

    def update(self):
        self.rect.x -= 5# я скорость x
        if self.rect.right < 0:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group, all_sprites)
        self.image = load_image('coin.png', color_key=-1)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height - 70
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


pygame.init()
size = w, h = (900, 700)
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()

tile_width = 50
tile_height = 50
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
treugs = pygame.sprite.Group()
floor_blocks = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

coin_count = 0
font = pygame.font.Font(None, 50)
# pygame.mixer.music.load('data/BackOnTrack.mp3')
# pygame.mixer.music.play(-1)

level_map = load_level('map.map')
player = generate_level(level_map)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    all_sprites.update()
    if pygame.sprite.spritecollideany(player, treugs, pygame.sprite.collide_mask):
        running = False

    stolcnov_coin = pygame.sprite.spritecollide(player, coins_group, True, pygame.sprite.collide_mask)
    if stolcnov_coin:
        coin_count += len(stolcnov_coin)

    coin_text = font.render(f'Coins: {coin_count}', False, (255, 255, 255))

    screen.fill((255, 0, 0))
    all_sprites.draw(screen)

    screen.blit(coin_text, (10, 10)) # рисует поверх экрана

    pygame.display.flip()
    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
