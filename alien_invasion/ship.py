import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the players ship"""

    def __init__(self, ai_game):
        """Initialize the shop and it's starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load picture of ship and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # place every new ship at the bottom midle screen
        self.rect.midbottom = self.screen_rect.midbottom

        # saves the value for the ship inside its middle
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """update the ship's position based on the movement flag"""
        # updates the value of the ship middle, not the one of the rectangle
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.y > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.y+50 < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # updates the rect object on the basis of self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """center the ship in the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.y = self.settings.screen_height - 50
        self.x = float(self.rect.x)

    def blitme(self):
        """draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
