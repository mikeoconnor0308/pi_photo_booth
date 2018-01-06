import pygame
from enum import Enum
import glob
import os


class Photo:
    """
    Container for representing a photo in the UI
    :type path: str
    
    """

    def __init__(self, path, unscaled_image, surface, coords):
        self.path = path
        self.unscaled_image = unscaled_image
        self.surface = surface
        self.coords = coords


class GamePhase(Enum):

    PREVIEWING = 1
    CAPTURING = 2
    REVIEWING = 3
    FILTERING = 4
    UPLOADING = 5


class PhotoboothGame:
    """
    Manages the pygame UI for photobooth. 
    """

    def previewing_phase(self):
        self.screen.fill(self.black)
        self.phase = GamePhase.PREVIEWING
        pygame.display.update()

    def capturing_phase(self):
        self.phase = GamePhase.CAPTURING
        self.screen.fill(self.black)
        pygame.display.update()

    def position_in_center(self, surface):
        yadjust = -50
        rect = surface.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.centery = self.screen.get_rect().centery + yadjust

        self.screen.blit(surface, rect)

    def reviewing_phase(self):
        self.phase = GamePhase.REVIEWING
        self.screen.fill(self.white)
        self.photo = pygame.image.load("{}/weddingshot.jpg".format(self.photo_dir)).convert()

        # scale and adjust image, then render it.
        w, h = self.photo.get_size()
        scale = 0.5

        self.photo = pygame.transform.scale(self.photo, (int(w * scale), int(h * scale)))
        self.position_in_center(self.photo)
        rect = self.photo.get_rect()

        # Render text beneath photo
        textsurface = self.font.render('Upload photo?', False, (120, 120, 120))
        text_rect = textsurface.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.centery = 15

        self.screen.blit(textsurface, text_rect)

        pygame.display.update()

    def load_images(self, path):
        # TODO generating images should be separated out from rendering them, so selection can work.
        self.images = []
        self.image_paths = ["{}/weddingshot.jpg".format(self.photo_dir)]
        filtered_images = glob.glob(os.path.join(path, "*.jpg"))
        self.image_paths.extend(filtered_images)

        size = 100
        spacing = 20
        screenwidth = self.screen.get_size()[0]
        # center filters
        x = (screenwidth - ((size + spacing) * len(self.image_paths))) / 2
        y = 360
        for image_file in self.image_paths:
            unscaled_image = pygame.image.load(image_file).convert()
            image = pygame.transform.scale(unscaled_image, (size, size))
            coords = (int(x), int(y))

            # self.screen.blit(image, coords)
            x += size + spacing
            photo = Photo(image_file, unscaled_image, image, coords)
            self.images.append(photo)

        self.current_filter_index = 0
        self.render_row(self.current_filter_index)

    def render_row(self, selected_index):
        """
        Renders the row of filtered images.
        :param path: path to filtered image. 
        :return: 
        """
        index = 0
        for image in self.images:
            # if image is the selected image, render border around it
            if index == selected_index:
                self.render_border(image.surface, image.coords)
            # otherwise just blit the image.
            else:
                self.screen.blit(image.surface, image.coords)
                self.add_surface_to_dirty(image.surface, image.coords)
                self.dirty_rects.append(image.surface.get_rect())
            index += 1

    def add_surface_to_dirty(self, surface, coords):
        """
        For a given surface being blitted to a particular point, marks the resulting rect as dirty.
        :param surface: 
        :param coords: 
        :return: 
        """
        rect = surface.get_rect()
        rect.x = coords[0]
        rect.y = coords[1]
        self.dirty_rects.append(rect)

    def render_border(self, surface, coords, border_width = 10):
        # copy the surface so we only temporarily add border.
        surf_copy = surface.copy()
        pygame.draw.rect(surf_copy, self.white, surface.get_rect(), border_width)
        pygame.draw.rect(surf_copy, self.green, surface.get_rect(), border_width - 3)
        self.screen.blit(surf_copy, coords)
        self.add_surface_to_dirty(surf_copy, coords)

    def filter_phase(self):
        """
        Moves to filter_phase
        :return: 
        """
        self.phase = GamePhase.FILTERING
        self.screen.fill(self.white)
        self.position_in_center(self.photo)
        self.load_images(os.path.join(self.photo_dir, "filtered"))

    def switch_to_phase(self, phase):

        if phase == GamePhase.PREVIEWING:
            self.previewing_phase()
        elif phase == GamePhase.CAPTURING:
            self.capturing_phase()
        elif phase == GamePhase.REVIEWING:
            self.reviewing_phase()
        elif phase == GamePhase.FILTERING:
            self.filter_phase()

    def update(self):
        pygame.display.update(self.dirty_rects)
        self.dirty_rects.clear()

    def __init__(self, photo_path):
        # set up game screen
        pygame.init()
        pygame.font.init()
        self.photo_dir = photo_path
        self.screen = pygame.display.set_mode((800, 480))
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.green = pygame.Color(46, 204, 64)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.dirty_rects = []
        self.previewing_phase()


