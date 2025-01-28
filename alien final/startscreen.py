import sys
import pygame as pg
from button import Button
from highscore_button import Highscore_Button
from pygame.sprite import Group
from settings import Settings
from colors import BLACK

class StartScreen():
    def __init__(self, theSettings, screen, button, highscore):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.theSettings = theSettings
        self.button = button
        self.highscore_button = highscore
        self.highscore_button_visible = True

        # Load alien images
        self.image = pg.image.load('images/alien01.png')
        self.image2 = pg.image.load('images/alien10.png')
        self.image3 = pg.image.load('images/alien21.png')
        self.image4 = pg.image.load('images/ufo.png')
        self.rect = self.image.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        # Set background color to black using BLACK from colors.py
        screen = pg.display.set_mode((self.theSettings.scr_width, self.theSettings.scr_height))
        screen.fill(BLACK)

    def makeScreen(self, theSettings, screen):
        pg.init()

        screen = pg.display.set_mode((theSettings.scr_width, theSettings.scr_height))
        pg.display.set_caption("Space Invaders")

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(BLACK)  # Set background to black

        # Display Space text
        font = pg.font.Font(None, 144)
        text1 = font.render("Space", 2, (255, 255, 255))
        textpos1 = text1.get_rect()
        textpos1.centerx = background.get_rect().centerx

        # Display Invaders text
        text2 = font.render("Invaders", 2, (0, 255, 0))
        textpos2 = ((theSettings.scr_width / 2) - 200, theSettings.scr_height / 6)

        # Alien position and text
        font = pg.font.Font(None, 44)

        text4 = font.render(" = 20 pts", 2, (250, 250, 250))
        textpos4 = text4.get_rect()

        text5 = font.render(" = 40 pts", 2, (250, 250, 250))
        textpos5 = text5.get_rect()
        
        text3 = font.render(" = 10 pts", 2, (250, 250, 250))
        textpos3 = text3.get_rect()
        
        text6 = font.render(" = ??????? pts", 2, (250, 250, 250))
        textpos3 = text6.get_rect()

        # Top alien
        textpos5 = ((theSettings.scr_width / 2) - 50, (theSettings.scr_height / 2) - 50)
        alienpos3 = ((theSettings.scr_width / 2) - 120, (theSettings.scr_height / 2) - 70)

        # Middle alien
        textpos3 = ((theSettings.scr_width / 2)- 50, (theSettings.scr_height / 2) + 10)
        alienpos1 = ((theSettings.scr_width / 2) - 120, (theSettings.scr_height / 2) - 10)

        # Bottom alien
        textpos4 = ((theSettings.scr_width / 2) - 50, (theSettings.scr_height / 2) + 70)
        alienpos2 = ((theSettings.scr_width / 2) - 120, (theSettings.scr_height / 2) + 50)
        
        #Mystery alien
        textpos6 = ((theSettings.scr_width / 2) - 70, (theSettings.scr_height / 2) + 120)
        alienpos4 = ((theSettings.scr_width / 2) - 130, (theSettings.scr_height / 2) + 100)

        # Draw onto screen
        background.blit(text1, textpos1)
        background.blit(text2, textpos2)
        background.blit(self.image, alienpos1)
        background.blit(self.image2, alienpos2)
        background.blit(self.image3, alienpos3)
        background.blit(self.image4, alienpos4)
        background.blit(text3, textpos3)
        background.blit(text5, textpos5)
        background.blit(text4, textpos4)
        background.blit(text6, textpos6)

        # Blit everything to screen
        screen.blit(self.image, (theSettings.scr_width / 2, theSettings.scr_height / 3))
        screen.blit(background, (200, 200))

        # Draw the play button on the start screen
        self.button.draw_button()
        if self.highscore_button_visible:  # Only draw if the button is visible
            self.highscore_button.draw_button()

        pg.display.flip()

        # Event handling for the start screen
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if self.button.rect.collidepoint(mouse_pos):
                        # Return from this function to start the game when the Play button is clicked
                        return
                    if self.highscore_button.rect.collidepoint(mouse_pos):
                        self._check_highscore_button(mouse_pos)
                        # Return from this function to display the high score when the High Score button is clicked

            # Keep drawing the button and background on the screen
            screen.blit(background, (0, 0))
            self.button.draw_button()
            if self.highscore_button_visible:
                self.highscore_button.draw_button()
            
            pg.display.flip()

    def _check_highscore_button(self, mouse_pos):
        if self.highscore_button_visible and self.highscore_button.rect.collidepoint(mouse_pos):
            print('Highscore button clicked')
            self.highscore_button_visible = False  # Hide the button
            self.display_highscore_text()  # Display the highscore text

    def display_highscore_text(self):
        try:
            # Open the file and read the text
            with open('highscore.txt', 'r') as file:
                highscore_text = file.read()
                highscore_text  = highscore_text + " is the best score!"
        except FileNotFoundError:
            highscore_text = "No highscore found."

        # Set the font and color for rendering the text
        font = pg.font.SysFont(None, 48)  # Adjust font size as needed
        text_color = (255, 255, 255)  # White text, customize as needed
        text_image = font.render(highscore_text, True, text_color)

        # Create a rect for positioning the text above the highscore button
        text_rect = text_image.get_rect()
        
        # Position the text where the highscore button was
        text_rect.centerx = self.highscore_button.rect.centerx
        text_rect.centery = self.highscore_button.rect.centery - 40  # Position it where the button was

        # Blit the text onto the screen
        self.screen.blit(text_image, text_rect)

        # Update the screen to show the text
        pg.display.flip()

        # Add a small delay so the player can read the highscore
        pg.time.wait(3000)  # Display the highscore for 3 seconds

        # After the delay, replace the text with the highscore button
        self.highscore_button_visible = True
        self.makeScreen(self.theSettings, self.screen)  # Go back to the start screen