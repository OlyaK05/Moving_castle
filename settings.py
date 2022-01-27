import os
import sys
import pygame
import sqlite3

pr_control = True
pygame.init()
size = width, height = 750, 700
screen = pygame.display.set_mode(size)


def text(message, x, y, font_size=75, font_type='shrift.otf', font_color=(255, 255, 255)):
    """функция вывода текста на surface"""
    if pr_control:
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
        self.con = sqlite3.connect("db_results.db")
        self.cur = self.con.cursor()

    def append_score(self, score, time):
        """добавление новых значений"""
        s = [score, time // 60]
        self.cur.execute("""INSERT INTO results VALUES (?, ?)""", s)
        self.con.commit()
        return

    def close_db(self):
        self.con.close()


def terminate(score=0, counter=0):
    global pr_control
    pr_control = False
    name = ""
    db = BaseDate()
    db.append_score(score, counter)
    db.close_db()
    pygame.quit()
    return False


arrow_sprite = pygame.sprite.Group()
Arrow(arrow_sprite)
