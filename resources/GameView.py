import os
import pandas as pd
from numpy import random
import json

from resources.Executioner import Executioner as Executioner
from resources.Victim import Victim as Victim

# Game View Class
class GameView:
    def __init__(self):
        os.system('cls||clear')
        self.loadJson()
        self.printTitle()
        self.play = True

    def loadJson(self):
        with open('resources/game_settings.json') as json_file:
            data = json.load(json_file)
        self.json = data

    def printTitle(self):
        
        title = self.json['title']
        print(title)

    def playAgain(self):
        again = input('Do you wish to play again? [Y]/n\n')
        if again == 'n':
            self.play = False
        elif again == 'c':
            self.repaintScreen()

    # Repaints screen
    def repaintScreen(self):
        os.system('cls||clear')
        self.printTitle()

    # Starts main game loop
    def playGame(self):
        while self.play == True:
            victim_obj = Victim()
            executioner = Executioner(self,victim_obj)
            executioner.startAsking()
            self.playAgain()
