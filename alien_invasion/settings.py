# Settings file for Alien Invasion
# by Auzmyn, 2021

class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings."""
        # Setting for screen resolution, ship and fleet speed
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.fleet_drop_speed = 10

        # sets acceleration of game
        self.speedup_scale = 1.1

        # increases points for hitting
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 48, 48)
        self.bullets_allowed = 3

    def initialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed = 0.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.4
        # the value 1 for fleet_direction means to the right, -1 to the left
        self.fleet_direction = 1
        # alien value
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings and alien points values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
