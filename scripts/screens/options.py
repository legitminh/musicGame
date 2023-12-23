import pygame
from interfaces import *
from UI import Button, ScrollBar
from .screen import Screen
from constants import *

class Options(Screen):
    mouse_down = False

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, **kwargs):
        super().__init__(screen, clock, **kwargs)
        self.user_interfaces = [
            Button(self.screen, [self.screen.get_width() / 2, 50], None, 'Options', 50),
            Button(self.screen, [self.screen.get_width() / 2, 125], None, 'Volume', 30)
        ]
        self.others = pygame.sprite.Group(self.user_interfaces)
        self.sound_slider = ScrollBar(self.screen, [25, 160], [self.screen.get_width() - 25, 180], [50, 20], 'black', 'dark gray',
                                orientation='horizontal', start_pos=[50 + (self.volume * (self.screen.get_width() - 150)), 160])
        self.sliders = pygame.sprite.Group(self.sound_slider)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise ExitException()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return Redirect(ScreenID.intro, volume=self.volume)
                elif event.type == pygame.VIDEORESIZE:
                    self._video_resize()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._left_click()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
            if self.mouse_down:
                self.sound_slider.click_drag(pygame.mouse.get_pos())
            self._draw()

    def _draw(self):
        self.screen.fill('light gray')
        self.volume = int(self.sound_slider.rect.topleft[0] - self.sound_slider.start_pos[0]) / (
                    self.sound_slider.end_pos[0] - self.sound_slider.start_pos[0] - self.sound_slider.rect.width)
        self.sliders.update(f'{int(self.volume * 100)}%', args_c='white')
        self.others.draw(self.screen)
        self.others.update()
        self.clock.tick(FRAME_RATE)
        pygame.display.update()

    def _video_resize(self):
        self.sound_slider.end_pos = self.screen.get_width() - 25, 180
        self.sound_slider.update(screen_change=True)
        leng = self.sound_slider.end_pos[0] - self.sound_slider.start_pos[0] - self.sound_slider.rect.width
        self.sound_slider.rect.topleft = self.sound_slider.start_pos[0] + (self.volume * leng), 160
        for sprite in self.user_interfaces:
            L = list(sprite.rect.center)
            L[0] = self.screen.get_width() / 2
            sprite.rect.center = L[0], L[1]

    def _left_click(self):
        clicked_pos = pygame.mouse.get_pos()
        if self.sound_slider.back_rect.collidepoint(clicked_pos):
            self.sound_slider.click_drag(clicked_pos)
            self.mouse_down = True
