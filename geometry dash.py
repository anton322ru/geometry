import os
import pygame


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
    return new_player

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height - self.rect.height
        self.y_player = 0
        self.on_ground = True

    def update(self):
        self.y_player += 0.7
        self.rect.y += self.y_player
        if self.rect.bottom >= h - 50:
            self.rect.bottom = h - 50
            self.on_ground = True
            self.y_player = 0

    def jump(self):
        if self.on_ground:
            self.y_player = -13
            self.on_ground = False

# Класс треугольника
class Treug(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(treugs, all_sprites)
        self.image = load_image('treug.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * tile_width
        self.rect.y = pos_y * tile_height - self.rect.height

    def update(self):
        self.rect.x -= 4 # я скорость x
        if self.rect.right < 0:
            self.kill()

pygame.init()
size = w, h = (800, 400)
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()

tile_width = 30
tile_height = 50
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
treugs = pygame.sprite.Group()

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
    if pygame.sprite.spritecollideany(player, treugs):
        running = False

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()