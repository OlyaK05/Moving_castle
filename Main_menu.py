import pygame

size = width, height = 600, 600
screen = pygame.display.set_mode(size)


class Button:
    def __init__(self, width, height):
        self.widht = width
        self.height = height
        self.inactive_color = (13, 102, 58)
        self.active_color = (13, 162, 58)

    def draw(self, x, y, message, action=True):
        pos = pygame.mouse.get_pos()  # координаты курсора
        click = pygame.mouse.get_pressed()  # нажатие на кнопку
        if x < pos[0] < x + self.widht and y < pos[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.widht, self.height))
                if click[0] == 1 and action is not None:  # нажатие на левую кнопку мыши
                    pygame.mixer.music.load("button_sound.mp3")
                    pygame.mixer.music.set_volume(0.04)
                    pygame.mixer.music.play(loops=0)

                    #action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.widht, self.height))
        text(message, x + 10, y + 10)


def text(message, x, y, font_color=(0,0,0), font_type='shrift.otf', font_size=100):
    front_type = pygame.font.Font(font_type, font_size)
    text = front_type.render(message, True, font_color)
    screen.blit(text, (x,y))