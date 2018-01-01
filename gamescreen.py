import pygame
from enum import Enum


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

    def reviewing_phase(self):
        self.phase = GamePhase.REVIEWING
        self.screen.fill(self.white)
        img = pygame.image.load("{}/weddingshot.jpg".format(self.photo_dir)).convert()

        # scale and adjust image, then render it.
        w, h = img.get_size()
        scale = 0.75
        yadjust = -50
        img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
        rect = img.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.centery = self.screen.get_rect().centery + yadjust
        self.screen.blit(img, rect)

        textsurface = self.font.render('Upload photo?', False, (120, 120, 120))
        textcoords = (rect.left, rect.bottom + 10)
        self.screen.blit(textsurface, textcoords)

        pygame.display.update()

    def __init__(self, photo_path):
        # set up game screen
        pygame.init()
        pygame.font.init()
        self.photo_dir = photo_path
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),
                                              pygame.FULLSCREEN)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        self.previewing_phase()


