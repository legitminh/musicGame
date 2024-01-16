import pygame
from editableTextBox import EditableTextBox
from iterfaces import Direction, Color
from scrollBar import ScrollBar
from box import Box
from listGroup import ListGroup
import sys


def main():
    pygame.init()
    pygame.key.set_repeat(250, 50)

    screen = pygame.display.set_mode([800, 500], pygame.RESIZABLE)

    list_group = ListGroup(
        10, *[
            Box(screen, lambda x, y: [200, 100], lambda x, y: [100, 50]), 
            Box(screen, lambda x, y: [200, 300], lambda x, y: [100, 50]), 
            Box(screen, lambda x, y: [200, 500], lambda x, y: [100, 50]), 
            Box(screen, lambda x, y: [200, 700], lambda x, y: [100, 50]), 
            Box(screen, lambda x, y: [200, 900], lambda x, y: [100, 50]), 
        ]
    )
    input_box = EditableTextBox(
        Box(screen, lambda x, y: (x / 2, y / 2), lambda x, y: (x / 5, 100), draw_from=Direction.center), 
        '<c:gray40, i>Place holder</>'
    )
    scroll_bar = ScrollBar(
        Box(screen, lambda x, y: [50, 50], lambda x, y: [50, y - 50], focused_color=Color('light gray')), 
        Box(screen, lambda x, y: [50, 50], lambda x, y: [50, 100], background_color=Color('dark gray')),
        list_group, 
        display_area=500, 
        display_percentage=True
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            input_box.update(event)
            list_group.update(event)
            scroll_bar.update(event)
        screen.fill('gray')
        input_box.draw()
        list_group.draw()
        scroll_bar.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
