import os
import pandas as pd
from numpy import random
import json

# Victim Class

class Victim:

    def __init__(self):
        self.loadVictimJson()
        self.max_lives = self.json['n_lives']
        self.frames = self.json['stages']
        self.current_life = 0
        self.alive = True

    def loadVictimJson(self):
        with open('resources/victim_settings.json') as json_file:
            data = json.load(json_file)
        self.json = data

    def loseLife(self):
        self.current_life += 1
        if self.current_life == self.max_lives:
            self.alive = False

    def printFrame(self):
        frame = self.frames[self.current_life]
        print(frame)