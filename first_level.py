import os
import sys
import pygame

pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Не найдено:/")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))  # самая длинная строка

    return list(map(lambda x: x.ljust(max_width, "."), level_map))  # ljust дополняем каждую строку до нужной длины

def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile('empty', x, y)
            elif level[y][x] == "#":
                Let('wall', x, y)
            elif level[y][x] == "*":
                Tile('lake', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                player = Player(x, y)
    return player, x, y

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Let(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_let_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y)
        self.x = 0
        self.y = 0

    def update(self, action):
        x, y = 0, 0
        if action[pygame.K_UP]:
            y = -25
        elif action[pygame.K_DOWN]:
            y = 25
        elif action[pygame.K_RIGHT]:
            x = 25
        elif action[pygame.K_LEFT]:
            x = -25
        self.rect = self.rect.move(x, y)
        self.rect.x += x
        self.rect.y += y
        if pygame.sprite.spritecollideany(self, tile_let_group) \
                or pygame.sprite.spritecollideany(self, horizontal_borders) \
                or pygame.sprite.spritecollideany(self, vertical_borders):
            self.rect = self.rect.move(-x, -y)
            self.rect.x -= x
            self.rect.y -= y


tile_images = {

    'empty': load_image("grass2.jpg"),  # элементы игрового поля
    'wall': load_image("wall.jpg"),
    'lake': load_image("lake.jpg"),
    # 'firewood': load_image("firewood.png")

}

player_image = load_image("fire.png")

all_sprites = pygame.sprite.Group()

tile_group = pygame.sprite.Group()
tile_let_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_width = tile_height = 50

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(-25, -25, width, -25)
Border(0, height + 25, width, height + 25)
Border(-25, 0, -25, height)
Border(width + 25, 0, width + 25, height)

player, level_x, level_y = generate_level(load_level("level.txt"))