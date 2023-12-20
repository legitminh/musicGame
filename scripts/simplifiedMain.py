"""
DEPRECATED
This script is the entire game runner, 
    consist of main loop that triggers individual scene loops that goes on until termination
"""
#imports
from scripts.UI import *
import pygame
from random import choice
from sys import exit

#global variables
songs = {0: 'Musics/Hot Cross Buns.wav', 1: 'Musics/Twinkle Twinkle Little Star.wav', 2: 'Musics/Happy Birthday.wav',
         3: 'Musics/Jingle Bells.wav', 4: 'Musics/Fur Elise.wav', 5: 'Musics/La Campanella.wav'}
requirements = {
    0: 0,
    1: 3,
    2: 5,
    3: 6,
    4: 7,
    5: 8
}
invrequirements = {v: k for k, v in requirements.items()} #inverse dictionary of requirements, 
clock = pygame.time.Clock()
volume = .2
high_scores = {}
parameters = str | int | float #possible game function parameters
mode_type = tuple[function, list[parameters]] #data type of mode

#initialization 
pygame.init()
screen = pygame.display.set_mode([799, 500], pygame.RESIZABLE)
pygame.display.set_caption("Typing piano")
img = pygame.image.load('Checkered pattern.png')
pygame.display.set_icon(img)
screen.fill('dark gray')

#main loop
def main():
    mode: mode_type #mode is a function in the gameplay loop with certain parameters, this defines what is happenining in the game
    # mode[0](*mode[1])  # call mode like this
    mode = (intro, [])

    loadPlayerData() #read saved player data into file
    while True:  # Playing >> End screen
        mode = mode[0](*mode[1])

#intro loop, render waiting scene until ending of game
def intro() -> mode_type:
    while True:
        #intro variables
        intro_g = pygame.sprite.Group()
        intro_l = [
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 - 50], None, 'Typing Piano', 50),
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 + 50], level_select, 'Play', 30),
            Button(screen, [screen.get_width() // 2, screen.get_height() // 2 + 100], options, 'Options', 30)
        ]
        intro_g.add(intro_l)

#end the game and save player data into file
def quitGame():
    savePlayerData()
    pygame.quit()
    exit()

#save player data
def savePlayerData() -> None:
    with open('PlayerData', mode='w') as f:
        write = ''
        for level_n, percent in high_scores.items():
            write += f'{level_n},{percent}\n'
        f.write(write)

#read player data and save it into high_scores
def loadPlayerData():
    global high_scores
    with open('PlayerData', mode='r') as f:
        for line in f.read().strip().split():
            high_scores[line.split(',')[0]] = float(line.split(',')[1])