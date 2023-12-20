import pygame
from interfaces import *

class Outro:
    def __init__(self,) -> None:
        pass
    def loop(level_num, score, slow_down):
        update_high_scores(level_num, score, slow_down)
        outro_g = pygame.sprite.Group()
        if isinstance(level_num, str):
            directory = songs[int(level_num.replace('e', '').replace('p', ''))]
        else:
            directory = songs[level_num]
        
        outro_l = [Button(screen, [screen.get_width() / 2, screen.get_height() // 2 + 50], level_num, 'Play again', 30),
                Button(screen, [screen.get_width() / 2, screen.get_height() // 2 - 50], '',
                        f'You scored {score:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                        30),
                Button(screen, [screen.get_width() / 2, screen.get_height() // 2 + 110], level_select,
                        'Return to level selection', 30)]
        outro_g.add(outro_l)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    file_writer()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return (level_select, [])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(len(outro_g.sprites())):
                            s = outro_g.sprites()[i]
                            pos = pygame.mouse.get_pos()
                            if s.rect.collidepoint(pos[0], pos[1]) and (
                                    isinstance(outro_l[i].mode_c, int) or outro_l[i].mode_c):
                                if isinstance(outro_l[i].mode_c, str):
                                    return (extreme_level, [outro_l[i].mode_c, slow_down])
                                if isinstance(outro_l[i].mode_c, int):
                                    return (level, [outro_l[i].mode_c, slow_down])
                                return (outro_l[i].mode_c, [])
            screen.fill('light gray')
            outro_g.draw(screen)
            outro_g.update()
            pygame.display.update()