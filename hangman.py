# Hangman Game
import os
import pandas as pd
from numpy import random
import json

# Setting up game view
class GameView:
    def __init__(self):
        os.system('cls||clear')
        self.printTitle()
        self.play = True

    def printTitle(self):
        title = open('resources/title.txt','r')
        title_lines = title.readlines()
        for line in title_lines:
            print(line[:-1])

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


class Executioner:

    def __init__(self,gameview,victim):
        self.view = gameview
        self.victim = victim
        self.loadWords()
        self.chooseWord()
        self.makeCharacterList()

        self.wrong_guesses = []
        self.correct_guesses = []
        self.proportion_correct = 0
        
    def loadWords(self):
        wordbank_location = 'resources/wordbank.txt'
        words_obj = pd.read_csv(wordbank_location).T.index
        words = [word for word in words_obj]
        self.words = words

    def chooseWord(self):
        number_of_words = len(self.words)
        index = random.randint(number_of_words)
        self.chosen_word = self.words[index]
        self.word_length = len(self.chosen_word)

    def makeCharacterList(self):
        character_list = []
        for character in self.chosen_word:
            if character in character_list:
                pass
            else:
                character_list.append(character)
        self.character_list = character_list

    def printGuesses(self):
        if len(self.wrong_guesses) == 0:
            print('')
        else:
            output_string = 'Guesses so far: '
            for guess in self.wrong_guesses:
                output_string = output_string + ' ' + guess
            print(output_string)
    
    def generateBlanksString(self):
        correct = self.correct_guesses
        output_string = ''
        n_correct = 0
        for space in range(self.word_length):
            guessed = False
            for character in correct:
                if character == self.chosen_word[space]:
                    output_string = output_string + ' ' + character
                    guessed = True
                    n_correct = n_correct + 1
            if guessed == False:
                output_string = output_string + ' _'
        self.proportion_correct = n_correct / self.word_length
        return output_string

    def printBlanks(self):
        output_string = self.generateBlanksString()
        print(output_string)
        
    def getGuess(self):
        guess = input('Please make a guess:\n')
        guess_validity = self.checkGuessCorrect(guess)
        if guess_validity == True:
            self.correct_guesses.append(guess)
        else:
            self.wrong_guesses.append(guess)

    def checkGuessCorrect(self,guess):        
        correct = False
        for character in self.chosen_word:
            if guess == character:
                return True
        if correct == False:
            self.victim.loseLife()
            return False

    def renderScreen(self):
        self.victim.printFrame()

    def startAsking(self):
        complete = False
        while complete == False:
            self.renderScreen()
            self.printGuesses()
            self.printBlanks()

            if self.proportion_correct == 1:
                print('Congratulations!  You have successfully guessed the correct answer!')
                break
            
            self.getGuess()

            if self.victim.alive == False:
                self.renderScreen()
                print('Too many guesses.  Your victim has died...')
                complete = True
            

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


# initiating GameView
game = GameView()
game.playGame()
