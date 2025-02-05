import os
import pygame

pygame.init()

w, h = 800, 600
FPS = 30
GRAVITY = 0.5

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

class Player:
    def __init__(self):
        self.image = load_image('mar.png')  # Загрузка изображения
        self.rect = self.image.get_rect(topleft=(100, h - 150))
        self.velocity_y = 0
        self.on_ground = False

    def jump(self):
        if self.on_ground:
            self.velocity_y = -10
            self.on_ground = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        if self.rect.y >= h - 100:
            self.rect.y = h - 100
            self.velocity_y = 0
            self.on_ground = True

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)  # Отображение изображения

class Prepitstv:
    def __init__(self, x):
        self.rect = pygame.Rect(x, h - 90, 20, 20)

    def update(self):
        self.rect.x -= 5

def main():
    pygame.display.set_caption("Geometry Dash Clone")
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()

    player = Player()
    rects = []
    score = 0
    spawn_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump()

        player.update()
        spawn_timer += 1
        if spawn_timer > 80:
            rects.append(Prepitstv(w))
            spawn_timer = 0

        for rect_1 in rects:
            rect_1.update()
            if rect_1.rect.x < 0:
                rects.remove(rect_1)
                score += 1

            if player.rect.colliderect(rect_1.rect):
                print("Game Over! Score:", score)
                running = False

        screen.fill((255, 255, 255))
        player.draw(screen)  # Отображение игрока
        for rect_1 in rects:
            pygame.draw.rect(screen, (255, 0, 0), rect_1.rect)

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print()

if __name__ == "__main__":
    main()

