import pygame
from .UI import UiElement, UiElementGroup


class ChooseOneGroup(UiElementGroup):
    def __init__(self, *args: UiElement | UiElementGroup):
        super().__init__(*args)

    def update(self, event: pygame.event.Event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            super().update(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            selected_element = None

            for element in self.elements:
                if element.is_hovered_over:
                    self.select_element(element)
                    selected_element = element
                    break
            return None if selected_element is None else selected_element.stored_value

    def select_element(self, element_to_select):
        for element in self.elements:
            if element is element_to_select:
                element.is_selected = True
            else:
                element.is_selected = False
