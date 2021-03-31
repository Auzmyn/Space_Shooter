import pygame


class Sound:
    """Class for sound effects"""

    def __init__(self):
        """Initialize the sound effects"""
        self.laser_soundfile = 'sounds/laserSmall_001.wav'
        self.ship_destroyed_soundfile = 'sounds/explosionCrunch_000.wav'

    def laser_sound(self):
        laser = pygame.mixer.Sound(self.laser_soundfile)
        laser_sound = pygame.mixer.Sound.play(laser)

    def ship_destroyed_sound(self):
        explosion = pygame.mixer.Sound(self.ship_destroyed_soundfile)
        ship_destroyed_sound = pygame.mixer.Sound.play(explosion)
