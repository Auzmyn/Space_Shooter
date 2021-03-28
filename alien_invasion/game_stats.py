class Gamestats:
    """trach statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        # starts the game in active mode
        self.game_active = False
        # highscore should never reset
        with open('highscore.txt') as file_object:
            content = file_object.read()
            content = int(content)
        self.high_score = content

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
