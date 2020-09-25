import os
import pandas as pd
from numpy import random
import json

# Executioner Class

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
        self.repeat = False
        
    def loadWords(self):
        choice = input('Please choose a difficulty. Easy or Hard: [E]/h\n')
        if choice == 'h':
            wordbank_location = 'resources/JSON/hard_words.json'
        elif choice == 'debug':
            wordbank_location = 'resources/JSON/debug_words.json'
        else:
            wordbank_location = 'resources/JSON/easy_words.json'
        
        with open(wordbank_location) as json_file:
            data = json.load(json_file)
        self.json = data
        self.words = data['words']

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
        if self.repeat == False:
            guess = input('Please make a guess:\n')
        else:
            guess = input('Previous guess was a repeat.  Please make a guess:\n')

        self.checkRepeat(guess)
        if self.repeat == False:
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

    def checkRepeat(self,guess):
        self.repeat = False
        if guess in self.wrong_guesses:
            self.repeat = True
        if guess in self.correct_guesses:
            self.repeat = True

    def renderScreen(self):
        self.view.repaintScreen()
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
                print('Too many guesses.  Your victim has died...  The correct word was {}'.format(self.chosen_word))
                complete = True
            
