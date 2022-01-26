import os
import sys
import pygame
import sqlite3

size = width, height = 750, 700
screen = pygame.display.set_mode(size)


def text(message, x, y, font_size=75, font_type='shrift.otf', font_color=(0, 0, 0)):
    """функция вывода текста на surface"""
    font_result = pygame.font.Font(font_type, font_size)
    texts = font_result.render(message, True, font_color)
    screen.blit(texts, (x, y))


def load_image(name, colorkey=None):
    """загрузка картинки из директории"""
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


def terminate():
    db.close_db()
    pygame.quit()
    return


arrow_sprite = pygame.sprite.Group()
Arrow(arrow_sprite)

name = ""
db = BaseDate()
