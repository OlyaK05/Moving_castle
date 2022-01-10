import pygame
import first_level
from  Main_menu import Button
running = True
button = Button(350, 200)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.key.get_pressed():
            first_level.all_sprites.update(pygame.key.get_pressed())
    first_level.tile_group.draw(first_level.screen)
    first_level.tile_let_group.draw(first_level.screen)
    first_level.player_group.draw(first_level.screen)
    button.draw(10, 50, "Moving castle")
    pygame.display.flip()
pygame.quit()
