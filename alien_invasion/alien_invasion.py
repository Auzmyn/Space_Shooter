# Alien Invasion, by Auzmyn 2021
# My first Python Game!

import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard
from sounds import Sound


class AlienInvasion:
    """Overall Class to manage game assets and behaviour"""

    def __init__(self):
        """Inititalize the game, and greate game resources"""
        pygame.init()
        self.settings = Settings()
        self.sound = Sound()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # builds an instance, to save game statistics and build a score rect
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # define back color
        self.bg_color = self.settings.bg_color

        # build a play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # sets settings back to default
            self.settings.initialize_dynamic_settings()
            # sets back statistic
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # removes mouse curser
            pygame.mouse.set_visible(False)

            # removes the alien ships and bullets
            self.aliens.empty()
            self.bullets.empty()

            # generates a new fleet and centers the own ship
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound.laser_sound()

    def _update_bullets(self):
        """update the position of the bullets and get rid of old bullets"""
        # updates the bullet position
        self.bullets.update()

        # removes bullets that hits the top of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collusions()

    def _check_bullet_alien_collusions(self):
        """Respond to bullet-allien collisions"""
        # checks if bullets hits an alien ship. If yes, bullet and ship will be removed
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # destroy all bullets and generate a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # set the level up
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """check if the fleet is at an edge, then updates the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # checks for collission between alien ship and your ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # check for aliens hittin te ground
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Creates the fleet of aliens"""
        # generate one alien ship and calculates the amount of ships per row
        # the gap between two ships is one alien ship
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # determine the amount of rows for the alien ships
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # generates the first row of alien ships
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """creates an alien an place it in row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """respond appropiately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # same reaction as a collusion with a alien
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        # reduce the number of left over ships and updates score table
        self.sound.ship_destroyed_sound()
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # eliminate all aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # generate a new fleet and ship
            self._create_fleet()
            self.ship.center_ship()

            # stops the game
            sleep(1)
        else:
            self.stats.game_active = False
            with open('highscore.txt', 'w') as file_object:
                file_object.write(str(self.sb.stats.high_score))
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on schreen and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # draws the score
        self.sb.show_score()

        # draws the play button only by inactive game
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # generate instance of game and runs it
    ai = AlienInvasion()
    ai.run_game()
