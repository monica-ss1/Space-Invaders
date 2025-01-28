import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
import os

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        filename = "highscore.txt"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                highscore = int(f.readline())
        else:
            highscore = 0
        self.high_score = int(highscore)

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score) + "\n")

