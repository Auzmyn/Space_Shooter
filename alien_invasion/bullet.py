# bullet file for alien_invasion ship
# by Auzmyn, 2021

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # generates a rectangle at position 0,0 and the moves it to the right position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # saves the position of the bullet as float
        self.y = float(self.rect.y)

    def update(self):
        """moves the bullet up the screen"""
        # updates the float position number of the bullet
        self.y -= self.settings.bullet_speed
        # updates the position of the rectangle
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
