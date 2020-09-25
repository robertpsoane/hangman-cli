# Hangman Game
import os
import pandas as pd
from numpy import random
import json

from resources.Classes.GameView import GameView as GameView

# initiating GameView
game = GameView()
game.playGame()