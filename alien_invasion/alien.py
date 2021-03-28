# alien ship
# by Auzmyn, 2021

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien"""

    def __init__(self, ai_game):
        """initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # loads the picture and get its rectanle ability
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # place a new invasionship at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # saves the position of the alien ship
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """move the alien to the right or left"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
