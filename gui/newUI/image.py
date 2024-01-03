""""
TODO: investigate how the image corners may be cut off through pillow or another image library.
"""
from box import Box
import pygame
from .UI import UiElement


class Image(UiElement):
    """An image drawn on top of a box."""
    def __init__(
            self,
            box: 'Box',
            image_path: str,
            blending_type: int = pygame.BLEND_RGBA_MAX,
            margin: int = 10,

            resize_image_to_box: bool = True,
            center_image_in_box: bool = True,
            keep_image_proportion: bool = True,
    ) -> None:
        super().__init__(box.display_surface, box.position_function, box.size_function)
        self.image_path = image_path
        self.blending_type = blending_type
        self.box = box
        self.margin = margin

        self.resize_image_to_box = resize_image_to_box
        self.center_image_in_box = center_image_in_box
        self.keep_image_proportion = keep_image_proportion

    def draw(self):
        if self.hidden:
            return

        self.box.draw()

        image = pygame.image.load(self.image_path)  # retrieving image
        if self.keep_image_proportion and self.resize_image_to_box:
            scale_up = min(
                (self.rect.width - self.margin) / image.get_width(),
                (self.rect.height - self.margin) / image.get_height()
            )
            image = pygame.transform.scale(image, image.get_rect().scale_by(scale_up, scale_up).size)
        elif self.resize_image_to_box:
            display_area = self.rect.width - self.margin, self.rect.height - self.margin
            image = pygame.transform.scale(image, display_area)  # scaling image
        image_size = image.get_size()  # getting size
        image = image.convert_alpha()  # removing transparent parts of image

        if self.center_image_in_box:  # centering the image
            pos = (self.rect.center[0] - image_size[0] / 2 + 1, self.rect.center[1] - image_size[1] / 2 + 1)
        else:  # putting the image on the top left
            pos = self.rect.topleft

        # rounding the corners of the image if it is resized
        flag = self.blending_type if self.resize_image_to_box else 0
        self.display_surface.blit(image, pos, None, flag)

    def update(self, event):
        self.box.update(event)
        super().update(event)

    def set_position(self, position: tuple[int, int]):
        self.box.set_position(position)

    def move(self, displacement: tuple[int, int]):
        self.box.move(displacement)
