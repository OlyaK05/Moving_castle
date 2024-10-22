import os
import pygame
import pygame_gui
from settings import load_image, width, height, arrow_sprite, text, screen, sound_button_click, control, save_results
pygame.init()
pygame.mouse.set_visible(False)

score = 0
counter = 0
received_pos = []
pr_control = True
level_names = ["level_1.txt", "level_2.txt", "level_3.txt"]
music_names = ["level_1.mp3", "level_2.mp3", "level_3.mp3"]
next_step = [12, 31, 54]


def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))  # самая длинная строка

    return list(map(lambda x: x.ljust(max_width, "."), level_map))  # дополняем каждую строку до нужной длины


def generate_level(level):
    x, y, player = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                BackGround('empty', x, y)
            elif level[y][x] == "#":
                Let('wall', x, y)
            elif level[y][x] == "*":
                Water('lake', x, y)
            elif level[y][x] == "a":
                Achievement('achievements', x, y)
            elif level[y][x] == "W":
                Finish('fireplace', x, y)
            elif level[y][x] == "@":
                BackGround('empty', x, y)
                player = Player(x, y)
    return player, x, y


class Border(pygame.sprite.Sprite):
    """границы карты"""

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


class Achievement(pygame.sprite.Sprite):
    """достижения"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(achievements_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class GaveAchievement(pygame.sprite.Sprite):
    """полученные достижения"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(gave_achievement)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x - 10, pos_y)


class BackGround(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(bg_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Let(pygame.sprite.Sprite):
    global control
    """расположение препятствий"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_let_group)
        if control % 2 == 0:
            self.image = load_image("wall.jpg")
        else:
            self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Water(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(water_let)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Finish(pygame.sprite.Sprite):
    """финишная черта"""

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(finish_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Player(pygame.sprite.Sprite):
    """класс героя"""

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y)
        self.rect.x = 10
        self.rect.y = 0

    def update(self, action):
        """перемещение героя по карте"""
        global score, control, counter
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
            self.rect = self.rect.move(-x, -y)  # при пересечении со спрайтами стенки/препятствия герой не двигается
            self.rect.x -= x
            self.rect.y -= y

        if pygame.sprite.spritecollideany(self, achievements_group):
            if (self.rect.x, self.rect.y) not in received_pos:
                fire_sound = pygame.mixer.Sound(os.path.join("music", "fire_sounds.mp3"))
                fire_sound.set_volume(0.04)
                fire_sound.play()
                score += 1
                received_pos.append((self.rect.x, self.rect.y))
            GaveAchievement('empty', self.rect.x, self.rect.y)
        if pygame.sprite.spritecollideany(self, water_let):
            counter += 267
        if pygame.sprite.spritecollideany(self, finish_group) and next_step[control - 1] == score:
            control += 1


tile_images = {

    'empty': load_image("grass.jpg"),  # элементы игрового поля
    'lake': load_image("lake.jpg"),
    'wall': load_image("wall_2.jpg"),
    'fireplace': load_image("fireplace.jpg"),
    'achievements': load_image("firewood.jpg")

}

player_image = load_image("fire.png")

player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bg_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
water_let = pygame.sprite.Group()
achievements_group = pygame.sprite.Group()
gave_achievement = pygame.sprite.Group()
tile_let_group = pygame.sprite.Group()

tile_width = tile_height = 50

# границы игрового поля
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Border(-25, -25, width, -25)
Border(0, height + 25, width, height + 25)
Border(-25, 0, -25, height)
Border(width + 25, 0, width + 25, height)


def level_controller():
    """generation level"""
    global control, level_names, pr_control, score, counter

    score = 0
    counter = 0
    if control == 1:
        if start_game(level_names[0], music_names[0]) == 0:
            return 0
    if control == 2:
        if start_game(level_names[1], music_names[1]) == 0:
            return 0
    if control == 3:
        if start_game(level_names[2], music_names[2]) == 0:
            return 0
    if pr_control:
        manager = pygame_gui.UIManager((width, height))
        menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (140, 50)),
                                                   text='back to menu',
                                                   manager=manager)
        result_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((600, 10), (140, 50)),
                                                     text='save results',
                                                     manager=manager)
        pygame.mixer.music.load(os.path.join("music", "end.mp3"))
        pygame.mixer.music.play(loops=-1)
        background = load_image("bg_end.jpg")
        clock = pygame.time.Clock()
        t = ""
        run = True
        while run:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    return 0
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    sound_button_click()
                    if event.ui_element == menu_button:
                        clear_sprites()
                        control = 1
                        return
                    if event.ui_element == result_button:
                        t = save_results(score, counter)
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    arrow_sprite.update(x, y)
                manager.process_events(event)
            if run:
                manager.update(time_delta)
                screen.blit(background, (0, 0))
                text("Game over", 190, 170, 120, font_color=(0, 0, 0))
                text(f"Your result", 230, 450, 90, font_color=(0, 0, 0))
                text(f"{counter//60} seconds", 290, 515, 80, font_color=(0, 0, 0))
                if t != "":
                    text(f"{t}seconds best result", 150, 300, 90, font_color=(0, 0, 0))
                manager.draw_ui(screen)
                if pygame.mouse.get_focused():
                    arrow_sprite.draw(screen)
                pygame.display.update()


def clear_sprites():
    bg_group.empty()
    achievements_group.empty()
    gave_achievement.empty()
    tile_let_group.empty()
    all_sprites.empty()
    player_group.empty()
    water_let.empty()
    finish_group.empty()


def start_game(level_name, music_name):
    """основная игра"""
    global counter, score, received_pos, pr_control

    pygame.mixer.music.load(os.path.join("music", music_name))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)

    player, x, y = generate_level(load_level(level_name))
    running = True
    received_pos = []
    start_control = control
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if start_control != control:
                clear_sprites()
                return
            if pygame.key.get_pressed():
                all_sprites.update(pygame.key.get_pressed())
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                arrow_sprite.update(x, y)
            if event.type == pygame.QUIT:
                running = False
                return 0
        if running:
            bg_group.draw(screen)
            achievements_group.draw(screen)
            gave_achievement.draw(screen)
            tile_let_group.draw(screen)
            water_let.draw(screen)
            finish_group.draw(screen)
            player_group.draw(screen)
            if pygame.mouse.get_focused():
                arrow_sprite.draw(screen)
            text(f"Time: {counter // 60}", 5, 5, 21, None)
            text(f"score: {score}", 85, 5, 21, None)
            counter += 1
            pygame.display.flip()
            clock.tick(60)
