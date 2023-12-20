import pygame
from interfaces import *


class Options:
    def options() -> mode_type:
        global volume
        sound_slider = ScrollBar(screen, [25, 160], [screen.get_width() - 25, 180], [50, 20], 'black', 'dark gray',
                                orientation='horizontal', start_pos=[50 + (volume * (screen.get_width() - 150)), 160])
        sliders = pygame.sprite.Group(sound_slider)
        user_interfaces = [
            Button(screen, [screen.get_width() / 2, 50], None, 'Options', 50),
            Button(screen, [screen.get_width() / 2, 125], None, 'Volume', 30)
        ]
        others = pygame.sprite.Group(user_interfaces)
        mouse_down = False
        while True:
            screen.fill('light gray')
            volume = int(sound_slider.rect.topleft[0] - sound_slider.start_pos[0]) / (
                        sound_slider.end_pos[0] - sound_slider.start_pos[0] - sound_slider.rect.width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    file_writer()
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    sound_slider.end_pos = screen.get_width() - 25, 180
                    sound_slider.update(screen_change=True)
                    leng = sound_slider.end_pos[0] - sound_slider.start_pos[0] - sound_slider.rect.width
                    sound_slider.rect.topleft = sound_slider.start_pos[0] + (volume * leng), 160
                    for sprite in user_interfaces:
                        L = list(sprite.rect.center)
                        L[0] = screen.get_width() / 2
                        sprite.rect.center = L[0], L[1]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked_pos = pygame.mouse.get_pos()
                        if sound_slider.back_rect.collidepoint(clicked_pos):
                            sound_slider.click_drag(clicked_pos)
                            mouse_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return (intro, [])
            if mouse_down:
                sound_slider.click_drag(pygame.mouse.get_pos())
            sliders.update(f'{int(volume * 100)}%', args_c='white')
            others.draw(screen)
            others.update()
            pygame.display.update()
