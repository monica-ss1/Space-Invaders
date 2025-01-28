import sys
import pygame as pg
from colors import OFF_WHITE, DARK_GREY
from settings import Settings
from ship import Ship
from vector import Vector
from fleet import Fleet
from game_stats import GameStats
from button import Button
from highscore_button import Highscore_Button
from scoreboard import Scoreboard
from event import Event
from barrier import Barriers
from sound import Sound
from startscreen import StartScreen
from ufo import UFO
import random

class AlienInvasion:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.sound = Sound()
        ufo_velocity = Vector(1, 0)  # Moving horizontally, for example
        self.ufo = UFO(self, ufo_velocity)
        self.ufo_dead_in_level = False
        self.last_ufo_time = 0  # Track time for UFO reappearance
        self.ufo_timer = 5000

        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(ai_game=self)
        self.high_score = GameStats(self)

        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.first = True

        self.play_button = Button(self, "Play")
        self.highscore_button = Highscore_Button(self, "High Score")
        self.event = Event(self)
        self.start_screen = StartScreen(self.settings, self.screen, self.play_button, self.highscore_button)

        # UFO random appearance timer
        self.ufo_visible = False  # To track if the UFO is currently visible
        self.ufo_timer = random.randint(500, 1500)  # Random interval for UFO appearance in milliseconds
        self.last_ufo_time = pg.time.get_ticks()  # Time when the UFO last appeared

    def game_over(self):
        print("Game over!") 
        self.sound.play_gameover()
        self.update_highscore()
        sys.exit()
        
    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True
        self.sound.play_background()
        self.fleet.more_aliens = True

        self.ship.reset_ship()
        self.fleet.reset_fleet()
        self.ufo_dead_in_level = False  # Reset UFO dead state for the new level
        pg.mouse.set_visible(False)
    
    def update_highscore(self):
    # Read the current high score from the file
        try:
            with open('highscore.txt', 'r') as file:
                current_high_score = file.read().strip()
                print(current_high_score)
        except FileNotFoundError:
            current_high_score = None

    # Get the new high score
        new_high_score = str(self.stats.high_score)

        if current_high_score == '':
            current_high_score = '0'

    # Compare and update if the new high score is higher
        if current_high_score.isdigit() and int(new_high_score) > int(current_high_score):
        
        # Clear the file and write the new high score
            with open('highscore.txt', 'w') as file:
                file.write(new_high_score)

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.play_button.reset_message("Play again? (q for quit)")
        self.reset_game()

    def run_game(self):
        self.finished = False
        self.first = True
        self.game_active = False
        self.start_screen.makeScreen(self.settings, self.screen)
        self.event.check_events()

        while not self.finished:
            self.finished = self.event.check_events()
            if self.first or self.game_active:
                self.first = False
                self.screen.fill(self.bg_color)
                self.ship.update()
                self.fleet.update()
                self.sb.show_score()
                self.barriers.update()

                # Check if it's time for the UFO to appear
                current_time = pg.time.get_ticks()
                if not self.ufo_visible and not self.ufo_dead_in_level and current_time - self.last_ufo_time > self.ufo_timer:
                    # Show the UFO
                    self.ufo_visible = True
                    self.ufo.rect.x = -70  # UFO starts from the left side
                    self.ufo.rect.y = 60  # Random vertical position
                    self.ufo.velocity = Vector(1, 0)  # Horizontal movement to the right

                # If the UFO is visible, update and draw it
                if self.ufo_visible:
                    self.ufo.update()  # Move the UFO
                    self.ufo.draw()    # Draw the UFO

                    # If UFO has moved off the screen, reset it
                    if self.ufo.rect.right > self.settings.scr_width:
                        self.ufo_visible = False
                        self.last_ufo_time = pg.time.get_ticks()
                        self.ufo_timer = random.randint(500, 1500)  # Set new random time for next UFO appearance
                    # Check for collisions between lasers and UFO
                    ufo_collision = pg.sprite.spritecollideany(self.ufo, self.ship.lasers)
                    if ufo_collision:
                        self.stats.score += 200  # Add 200 points to the score
                        self.sb.check_high_score()  # Check and update the high score if necessary
                        ufo_collision.kill()  # Remove the laser that hit the UFO
                        self.ufo.destroy()  # Trigger the destruction sequence

                        self.ufo_dead_in_level = True
                        self.last_ufo_time = pg.time.get_ticks()  # Reset the UFO timer
            if not self.game_active:
                self.play_button.draw_button()
            pg.display.flip()

            self.clock.tick(60)  # Keep the frame rate at 60 FPS

        sys.exit()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()