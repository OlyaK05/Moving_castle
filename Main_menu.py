import os
import sys
import pygame
import webbrowser
import first_level
import sqlite3

pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moving Castle")


def text(message, x, y, font_size=75, font_type='shrift.otf', font_color=(0, 0, 0)):
    pygame.init()
    """функция вывода текста на surface"""
    font_result = pygame.font.Font(font_type, font_size)
    texts = font_result.render(message, True, font_color)
    screen.blit(texts, (x, y))


def load_image(name, colorkey=None):
    """загрузка изображений из директории data"""
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


class BaseDate:
    """работа с базой данных"""

    def __init__(self):
        self.con = sqlite3.connect("DB_results.db")
        self.cur = self.con.cursor()

    def append_and_get_best_score(self, score, time):
        """добавление новых значений и возвращение лучшего результата"""
        s = [score, time]
        self.cur.execute("""INSERT INTO results VALUES (?, ?)""", s)
        result = self.cur.execute("""SELECT Score, Time FROM results """).fetchall()
        self.con.commit()
        return sorted(result, key=lambda x: (x[0], -x[1]), reverse=True)[0]

    def close_db(self):
        self.con.close()


name = ""
db = BaseDate()


class Arrow(pygame.sprite.Sprite):
    """класс курсора"""

    image = load_image("mouse.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        super().__init__(*group)
        self.image = Arrow.image
        self.rect = self.image.get_rect()
        self.rect.x = -20
        self.rect.y = 0

    def update(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.rect = self.rect.move(x - self.rect.x, y - self.rect.y)


class Button():
    """класс кнопок"""

    def __init__(self, width, height, sign):
        self.widht = width
        self.height = height
        self.inactive_color = (0, 107, 83)
        self.active_color = (0, 164, 127)
        self.sign = sign

    def draw(self, x, y, message, font_size=75):
        pos = pygame.mouse.get_pos()  # координаты курсора
        click = pygame.mouse.get_pressed()  # нажатие на кнопку
        if x < pos[0] < x + self.widht and y < pos[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.widht, self.height))
            if click[0] == 1:  # нажатие на левую кнопку мыши
                button_sound = pygame.mixer.Sound("button_sound.mp3")
                button_sound.play()
                if self.sign == 0:
                    start_first_game()
                elif self.sign == 1:
                    info()
                elif self.sign == 2:
                    webbrowser.open('https://ru.wikipedia.org/wiki/%D0%A5%D0%BE%D0%B4%D1%8F%D1%87%D0%B8%D0%B9_%D0%B7%D0'
                                    '%B0%D0%BC%D0%BE%D0%BA_(%D0%B0%D0%BD%D0%B8%D0%BC%D0%B5)', new=2)
                elif self.sign == 3:
                    menu()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10, font_size)


def menu():
    """основное меню игры"""
    pygame.mouse.set_visible(False)
    background = load_image("bg (1).jpg")
    pygame.mixer.music.load("sky_walk.mp3")
    pygame.mixer.music.play(loops=-1)

    button_start = Button(130, 100, 0)
    button_info = Button(130, 100, 1)
    button_story = Button(80, 65, 2)

    all_sprites = pygame.sprite.Group()
    arrow = Arrow(all_sprites)
    demonstration = True
    while demonstration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                demonstration = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                all_sprites.update(x, y)
        screen.blit(background, (0, 0))
        text("Moving Castle,", 200, 70, 100)
        button_start.draw(300, 270, "Start", 70)
        button_info.draw(300, 390, "Info", 70)
        button_story.draw(10, 600, "Story", 40)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


def info():
    screen.fill((0, 0, 0))
    background = load_image("background_info.jpg")
    running = True
    button_enter = Button(70, 60, 3)
    all_sprites = pygame.sprite.Group()
    arrow = Arrow(all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                all_sprites.update(x, y)
        screen.blit(background, (0, 0))
        button_enter.draw(675, 10, "Enter", 40)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


def start_first_game():
    """первый уровень"""
    screen.fill((0, 0, 0))
    all_sprites = pygame.sprite.Group()
    arrow = Arrow(all_sprites)
    counter, score, run = 0, first_level.score, first_level.run
    first_level.player, first_level.level_x, first_level.level_y = first_level.generate_level(first_level.load_level("level.txt"))
    clock = pygame.time.Clock()
    music_main = pygame.mixer.music.load("first_game.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db.close_db()
                running = False
            if pygame.key.get_pressed():
                first_level.all_sprites.update(pygame.key.get_pressed())
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                all_sprites.update(x, y)
        score, run = first_level.score, first_level.run
        first_level.tile_group.draw(first_level.screen)
        first_level.achievements_group.draw(first_level.screen)
        first_level.gave_achievement.draw(first_level.screen)
        first_level.tile_let_group.draw(first_level.screen)
        first_level.player_group.draw(first_level.screen)
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)
        text(f"Time: {counter // 60}", 5, 5, 21, None, (255, 255, 255))
        text(f"score: {score}", 85, 5, 21, None, (255, 255, 255))
        counter += 1

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

menu()
