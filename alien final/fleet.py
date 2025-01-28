import pygame as pg
from vector import Vector
from point import Point
from laser import Laser

from alien import Alien
from pygame.sprite import Sprite
from settings import Settings
from sound import Sound

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.fleet_lasers = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)  # Movement vector
        self.spacing = 1.4  # Spacing between aliens
        self.create_fleet()
        self.Settings = Settings()
        self.less_aliens = True
        self.more_aliens = True
        self.current_speed = 1
        self.sound = Sound()
    

    def reset_fleet(self):
        """Empty the aliens group and recreate the fleet."""
        self.aliens.empty()  # Clear the aliens
        self.counter = 0  # Reset the counter
        self.create_fleet()  # Recreate the fleet

    def create_fleet(self):
        """Create the entire fleet of aliens."""
        # Only create aliens in this method, no need to create one just for dimensions
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_height = alien.rect.height
        alien_width = alien.rect.width  # Use alien dimensions to space them out

        current_y = alien_height  # Start creating aliens vertically
        while current_y < (self.settings.scr_height - self.spacing * 6 * alien_height):
            self.create_row(current_y, alien_width)
            current_y += self.spacing * alien_height
        self.counter = 36

    def create_row(self, y, alien_width):
        """Create a row of aliens at a specific vertical position (y)."""
        current_x = alien_width  # Starting position for x

        # Only create aliens in this method
        while current_x < (self.settings.scr_width - alien_width):
            new_alien = Alien(self, v=self.v)  # Create a new alien
            new_alien.rect.y = y
            new_alien.y = y
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)  # Add to the alien group
            current_x += self.spacing * alien_width

    def check_edges(self):
        """Check if any alien is at the screen edges."""
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False
    
    def check_bottom(self):
        """Check if any alien has reached the bottom of the screen."""
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False
    
    def update(self):
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    self.stats.score += alien.points
            self.sb.check_high_score()
            
        if self.less_aliens:
            if len(self.aliens) < 20:
                self.sound.play_faster()
                self.fleet_lasers.empty()
                self.current_speed = self.v.x
                print(self.current_speed)
                self.v.x *=2
                self.less_aliens = False
                
        if self.more_aliens:
            if len(self.aliens)>= 20:
                self.v.x  = self.current_speed
                self.current_speed = self.v.x
                self.more_aliens = False
            
        if len(self.aliens) == 0:
            self.v.x  = self.current_speed * 1.3
            self.current_speed = self.v.x
            self.less_aliens = True
            self.sound.stop_faster()
            self.sound.play_background()
             # UFO reset logic: hide UFO and reset its state
            self.ai_game.ufo_visible = False  # Ensure UFO is not visible at the start of a new level
            self.ai_game.ufo_dead_in_level = False  # Allow UFO to appear in the new level
            self.ai_game.last_ufo_time = pg.time.get_ticks()
            self.ship.lasers.empty()
            self.create_fleet()
            self.stats.level += 1
            self.sb.prep_level()
            return

        if pg.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!")
            self.ship.ship_hit()
            self.v.x = self.current_speed
            return

        if self.check_bottom():
            return

        if self.check_edges():
            self.v.x *= -1
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed

        for alien in self.aliens:
            alien.update()
        
    def draw(self): 
        # Pass as draw method is not yet implemented
        pass
