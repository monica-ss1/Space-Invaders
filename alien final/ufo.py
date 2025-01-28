import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class UFO(Sprite):
    ufo_image = pg.image.load("images/ufo.png")
    ufo_destroyed_image = pg.image.load("images/ufo_200.png")  # Corrected file name

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v

        # Load the UFO image and set timers for destruction
        self.timer = Timer(images=[UFO.ufo_image], delta=0)
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        # Starting position of the UFO
        self.rect.x = -self.rect.width  # Start off-screen on the left
        self.rect.y = randint(50, 150)  # Random vertical position between 50 and 150
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dying = False
        self.dead = False
        self.active = False

        self.destroy_timer = None  # Timer for displaying the destruction image

        # Random interval for the UFO to appear
        self.appear_interval = randint(800, 1200)  # UFO appears after this many frames
        self.frames_since_last_appearance = 0

    def update(self):
        if self.dying:
            # If the UFO is in the "destroyed" state, show the destroyed image for 500 ms
            current_time = pg.time.get_ticks()
            if current_time - self.destroy_timer < 100:  # Display destruction image for 500 ms
                self.image = UFO.ufo_destroyed_image
            else:
                # After 500 ms, deactivate the UFO and reset
                self.dying = False
                self.dead = True
                self.active = False
                self.rect.x = -self.rect.width
        elif not self.active:
            # Count frames until the UFO appears
            self.frames_since_last_appearance += 1
            if self.frames_since_last_appearance >= self.appear_interval:
                self.active = True
                self.rect.x = -self.rect.width  # Reset to start from the left
                self.rect.y = randint(50, 150)  # Random y-position
                self.frames_since_last_appearance = 0
        else:
            # Move UFO across the screen
            self.rect.x += self.v.x

            # Check if UFO is off the screen
            if self.rect.x > self.ai_game.settings.scr_width:
                self.active = False
                self.appear_interval = randint(800, 1200)  # Set a new random interval
        
        if not self.dying:
            self.image = self.timer.current_image()
        
        if self.active or self.dying:  # Ensure UFO is drawn even during the dying state
            self.draw()

    def destroy(self):
        """Destroy the UFO and trigger the display of the destruction image."""
        self.dying = True
        self.destroy_timer = pg.time.get_ticks()  # Start the destruction timer

    def draw(self): 
        self.screen.blit(self.image, self.rect)