import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
screen_width = 864
screen_height = 936

# Puts the dimensions together and displays the caption on the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#load images
bg = pygame.image.load('img/bg.png')

# This `run` variable should be consistantly running so that our screen will persist.
run = True

# while `run` = True, run the game
while run:

  # display the background image on the screen.
  screen.blit(bg,(0,0))

  # This creates the 'exit' game and allows us to close the game.
  for event in pygame.event.get():
    if event.type ==pygame.QUIT:
      run = False

  # This continuously updates the display of the screen after each loop in the while loop.
  pygame.display.update()

# exiting the while loop for `run` means we'll hit this quit() function and close the application.
pygame.quit()