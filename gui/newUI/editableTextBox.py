"""
TODO: add max characters/words
TODO: support new line characters
TODO: add cursor color and cursor width as parameters
"""
from textBox import TextBox
import pygame
from time import time


class EditableTextBox(TextBox):
    user_text: str = ''
    PROMPT: str = None
    last_time_wrote: float = time()
    displayed_text: tuple[str, bool] = ()

    def update(self, event: pygame.event.Event):
        if self.PROMPT is None:
            self.PROMPT = self.text

        self.box.update(event)
        super().update(event)

        if event.type == pygame.KEYDOWN:
            if not self.box.is_selected:
                return
            self.last_time_wrote = time()
            if event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else:
                self.user_text += event.unicode
        if self.box.is_selected or self.user_text:
            if self.displayed_text == (self.user_text, False):
                return
            self.displayed_text = (self.user_text, False)
            self.set_text(self.user_text)
            self.set_process_text(False)
        else:
            if self.displayed_text == (self.PROMPT, True):
                return
            self.displayed_text = (self.PROMPT, True)
            self.set_text(self.PROMPT)
            self.set_process_text(True)

    def draw(self):
        if self.hidden: 
            return

        super().draw()

        if self.box.is_selected:
            if self.text:
                cursor_height = self._images_by_line[-1][-1].get_height()
                text_height = sum(max(img.get_height() for img in line) for line in self._images_by_line[:-1])
                cursor_top_left = self._images_by_line[-1][-1].get_width() / 2 + self.box.rect.centerx, -cursor_height / 2 + text_height / 2 + self.box.rect.centery
            else:
                cursor_height = self.render_text('1', self.default_properties).get_height()
                cursor_top_left = self.box.rect.centerx, self.box.rect.centery - cursor_height / 2
            CURSOR_WIDTH = 2
            if (time() - self.last_time_wrote) % 1 < 0.5:
                rect = pygame.Rect(*cursor_top_left, CURSOR_WIDTH, cursor_height)
                pygame.draw.rect(self.display_surface, "black", rect)
