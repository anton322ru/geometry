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
            elif level[y][x] == 'f':
                Finish(x, y)
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
        self.jumping = False

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
            self.kill()

    def jump(self):
        if self.on_ground:
            self.gravita = -15
            self.on_ground = False
            self.jumping = True

    def stop_jump(self):
        self.jumping = False

class Treug(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(treugs, all_sprites)
        self.image = load_image('treug.png', color_key=-1)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global speed
        self.rect.x -= speed  # я скорость x
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
        global speed
        self.rect.x -= speed  # я скорость x
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
        global speed
        self.rect.x -= speed  # я скорость x
        if self.rect.right < 0:
            self.kill()

class Finish(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = load_image('finish.png', color_key=-1)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global speed
        self.rect.x -= speed  # я скорость x
        if self.rect.right < 0:
            self.kill()

def draw_main_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 75)
    text = font.render('Главное меню', True, (255, 255, 255))
    text_rect = text.get_rect(center=(w // 2, h // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 50)
    start_text = font.render('Начать игру', True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(w // 2, h // 2 + 50))
    screen.blit(start_text, start_rect)

    total_coins_text = font.render(f'Всего монет: {total_coins}', True, (255, 255, 255))
    total_coins_rect = total_coins_text.get_rect(center=(w // 2, h // 2 + 150))
    screen.blit(total_coins_text, total_coins_rect)

    pygame.display.flip()
    return start_rect

def draw_level_select():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 75)
    text = font.render('Выбор уровня', True, (255, 255, 255))
    text_rect = text.get_rect(center=(w // 2, h // 2 - 150))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 50)
    level1_text = font.render('Уровень 1', True, (255, 255, 255))
    level1_rect = level1_text.get_rect(center=(w // 2, h // 2 - 50))
    screen.blit(level1_text, level1_rect)

    level2_text = font.render('Уровень 2', True, (255, 255, 255))
    level2_rect = level2_text.get_rect(center=(w // 2, h // 2 + 50))
    screen.blit(level2_text, level2_rect)

    level3_text = font.render('Уровень 3', True, (255, 255, 255))
    level3_rect = level3_text.get_rect(center=(w // 2, h // 2 + 150))
    screen.blit(level3_text, level3_rect)

    pygame.display.flip()
    return level1_rect, level2_rect, level3_rect

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
finish_group = pygame.sprite.Group()

coin_count = 0
total_coins = 0
font = pygame.font.Font(None, 50)

# Главный экран
main_menu = True
level_select = False
running = True
selected_level = None

while main_menu:
    start_rect = draw_main_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                main_menu = False
                level_select = True

while level_select:
    level1_rect, level2_rect, level3_rect = draw_level_select()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level_select = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if level1_rect.collidepoint(event.pos):
                speed = 5
                selected_level = 'map1.map'
                level_select = False
            elif level2_rect.collidepoint(event.pos):
                speed = 6
                selected_level = 'map2.map'
                level_select = False
            elif level3_rect.collidepoint(event.pos):
                speed = 8
                selected_level = 'map3.map'
                level_select = False

if running and selected_level:
    while running:
        level_map = load_level(selected_level)
        player = generate_level(level_map)

        space_pressed = False
        level_running = True
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    level_running = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                        player.jump()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_pressed = False
                        player.stop_jump()

            if space_pressed and player.jumping:
                player.jump()

            if pygame.sprite.spritecollideany(player, treugs, pygame.sprite.collide_mask) or not player.alive():
                level_running = False
                coin_count = 0

            stolcnov_coin = pygame.sprite.spritecollide(player, coins_group, True, pygame.sprite.collide_mask)
            if stolcnov_coin:
                coin_count += len(stolcnov_coin)

            if pygame.sprite.spritecollideany(player, finish_group, pygame.sprite.collide_mask):
                total_coins += coin_count
                level_running = False
                main_menu = True
                level_select = False
                coin_count = 0

            all_sprites.update()

            coin_text = font.render(f'Coins: {coin_count}', False, (255, 255, 255))

            screen.fill((255, 0, 0))
            all_sprites.draw(screen)

            screen.blit(coin_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        for sprite in all_sprites:
            sprite.kill()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()