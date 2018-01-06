import pygame
from enum import Enum
import glob
import os


class Photo:
    """
    Container for representing a photo in the UI
    """

    def __init__(self, path, unscaled_image, image, coords):
        self.path = path
        self.unscaled_image = unscaled_image
        self.image = image
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

    def select_image(self, index):
        """
        Highlights an image, and renders it in the middle.
        :param index: 
        :return: 
        """
        #TODO render square at selected image location, then call render_row

    def render_row(self, path):
        """
        Renders the row of filtered images.
        :param path: path to filtered image. 
        :return: 
        """
        #TODO generating images should be separated out from rendering them, so selection can work.
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
            self.screen.blit(image, coords)
            x += size + spacing
            photo = Photo(image_file, unscaled_image, image, coords)
            self.images.append(photo)

        self.current_filter_index = 0
        self.select_image(0)

    def filter_phase(self):
        """
        Moves to filter_phase
        :return: 
        """
        self.phase = GamePhase.FILTERING
        self.screen.fill(self.white)
        self.position_in_center(self.photo)
        self.render_row(os.path.join(self.photo_dir, "filtered"))
        pygame.display.update()

    def switch_to_phase(self, phase):

        if phase == GamePhase.PREVIEWING:
            self.previewing_phase()
        elif phase == GamePhase.CAPTURING:
            self.capturing_phase()
        elif phase == GamePhase.REVIEWING:
            self.reviewing_phase()
        elif phase == GamePhase.FILTERING:
            self.filter_phase()

    def __init__(self, photo_path):
        # set up game screen
        pygame.init()
        pygame.font.init()
        self.photo_dir = photo_path
        self.screen = pygame.display.set_mode((800, 480))
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.previewing_phase()


