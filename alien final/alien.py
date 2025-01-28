import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]
    alien_points = [10, 20, 40]  # Points for each alien type
    
    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v

        # Choose alien type randomly (0, 1, or 2)
        self.type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[self.type], delta=(self.type+1)*600, start_index=self.type % 2)
        self.image = self.timer.current_image()
        print(self.image)
        self.rect = self.image.get_rect()

        # Assign points based on alien type
        self.points = Alien.alien_points[self.type]

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.dying = False
        self.dead = False


    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        return self.x + self.rect.width >= sr.right or self.x <= 0

    def update(self):
        self.x += self.v.x
        self.y += self.v.y
        self.image = self.timer.current_image()
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()