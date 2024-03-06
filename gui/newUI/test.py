import pygame
from editableTextBox import EditableTextBox
from gui.newUI.interfaces import Direction, Color
from scrollBar import ScrollBar
from box import Box
from listGroup import ListGroup
import sys


def main():
    pygame.init()
    pygame.key.set_repeat(250, 50)

    screen = pygame.display.set_mode([800, 500], pygame.RESIZABLE)

            # TODO: figure out why EditableTextBoxes don't work with the scroll bar
            # EditableTextBox(Box(screen, lambda x, y: [200, 50], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 100], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 150], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 200], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 250], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 300], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 350], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 400], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 450], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 500], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 550], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 600], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 650], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 700], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 750], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 800], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 850], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 900], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 950], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 1000], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 1050], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 1100], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 1150], lambda x, y: [100, 50]), "asdf"),
            # EditableTextBox(Box(screen, lambda x, y: [200, 1200], lambda x, y: [100, 50]), "asdf"),
            # Box(screen, lambda x, y: [200, 50], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 100], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 150], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 200], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 250], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 300], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 350], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 400], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 450], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 500], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 550], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 600], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 650], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 700], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 750], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 800], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 850], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 900], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 950], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 1000], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 1050], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 1100], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 1150], lambda x, y: [100, 50]),
            # Box(screen, lambda x, y: [200, 1200], lambda x, y: [100, 50]),
    list_group = ListGroup(
        10, *[
            EditableTextBox(Box(screen, lambda x, y: [200, 50], lambda x, y: [100, 50]), "1"),
            EditableTextBox(Box(screen, lambda x, y: [200, 100], lambda x, y: [100, 50]), "2"),
            EditableTextBox(Box(screen, lambda x, y: [200, 150], lambda x, y: [100, 50]), "3"),
            EditableTextBox(Box(screen, lambda x, y: [200, 200], lambda x, y: [100, 50]), "4"),
            EditableTextBox(Box(screen, lambda x, y: [200, 250], lambda x, y: [100, 50]), "5"),
            EditableTextBox(Box(screen, lambda x, y: [200, 300], lambda x, y: [100, 50]), "6"),
            EditableTextBox(Box(screen, lambda x, y: [200, 350], lambda x, y: [100, 50]), "7"),
            EditableTextBox(Box(screen, lambda x, y: [200, 400], lambda x, y: [100, 50]), "8"),
            EditableTextBox(Box(screen, lambda x, y: [200, 450], lambda x, y: [100, 50]), "9"),
            EditableTextBox(Box(screen, lambda x, y: [200, 500], lambda x, y: [100, 50]), "10"),
            EditableTextBox(Box(screen, lambda x, y: [200, 550], lambda x, y: [100, 50]), "11"),
            EditableTextBox(Box(screen, lambda x, y: [200, 600], lambda x, y: [100, 50]), "12"),
            EditableTextBox(Box(screen, lambda x, y: [200, 650], lambda x, y: [100, 50]), "13"),
            EditableTextBox(Box(screen, lambda x, y: [200, 700], lambda x, y: [100, 50]), "14"),
            EditableTextBox(Box(screen, lambda x, y: [200, 750], lambda x, y: [100, 50]), "15"),
            EditableTextBox(Box(screen, lambda x, y: [200, 800], lambda x, y: [100, 50]), "16"),
            EditableTextBox(Box(screen, lambda x, y: [200, 850], lambda x, y: [100, 50]), "17"),
            EditableTextBox(Box(screen, lambda x, y: [200, 900], lambda x, y: [100, 50]), "18"),
            EditableTextBox(Box(screen, lambda x, y: [200, 950], lambda x, y: [100, 50]), "19"),
            EditableTextBox(Box(screen, lambda x, y: [200, 1000], lambda x, y: [100, 50]), "asdf"),
            EditableTextBox(Box(screen, lambda x, y: [200, 1050], lambda x, y: [100, 50]), "asdf"),
            EditableTextBox(Box(screen, lambda x, y: [200, 1100], lambda x, y: [100, 50]), "asdf"),
            EditableTextBox(Box(screen, lambda x, y: [200, 1150], lambda x, y: [100, 50]), "asdf"),
            EditableTextBox(Box(screen, lambda x, y: [200, 1200], lambda x, y: [100, 50]), "asdf"),
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
        display_area_func=lambda x, y: y - list_group.top, 
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
            scroll_bar.update(event)
            list_group.update(event)
        screen.fill('gray')
        input_box.draw()
        scroll_bar.draw()
        list_group.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
