import pygame
from gui.newUI.editableTextBox import EditableTextBox
from iterfaces import Direction
from box import Box
import sys


def main():
    pygame.init()
    pygame.key.set_repeat(250, 50)

    screen = pygame.display.set_mode([800, 500], pygame.RESIZABLE)

    input_box = EditableTextBox(
        Box(screen, lambda x, y: (x / 2, y / 2), lambda x, y: (x / 5, 100), draw_from=Direction.center), 
        '<c:gray, i>Place holder</>'
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
        screen.fill('gray')
        input_box.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
