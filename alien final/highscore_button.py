import pygame.font
from button import Button

import pygame

class Highscore_Button(Button):
    def __init__(self, ai_game, msg, width=200, height=50, button_color=(0, 135, 0), text_color=(255, 255, 255)):
        """Initialize highscore button attributes."""
        # Call the parent class's constructor
        super().__init__(ai_game, msg)  # Initialize the parent class (Button)
        self.rect.centery +=30
        # Set up the screen and screen rect
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Button size and properties
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 48)  # Make sure font module is initialized
        
        # Create the button's rect and center it horizontally
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx  # Center horizontally
        self.rect.centery = self.screen_rect.bottom - 40  # Position 70 pixels from the bottom

        # Prepare the button message (render text)
        self._prep_msg(msg)

    def reset_message(self, msg="High Score"):
        """Reset the message displayed on the button."""
        self.msg = msg
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Render the message text into an image and center it on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # Center the message on the button

    def draw_button(self):
        """Draw the button with the message on the screen."""
        self.screen.fill(self.button_color, self.rect)  # Draw the button rectangle
        self.screen.blit(self.msg_image, self.msg_image_rect)  # Draw the message text on the button