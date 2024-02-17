import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
screen_width = 864
screen_height = 936

# Puts the dimensions together and displays the caption on the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# This adds timing for the game's clock (helps with the scroll speed that we set below)
clock = pygame.time.Clock()
fps = 50

# define game variables
ground_scroll = 0
scroll_speed = 4

#load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

# This `run` variable should be consistantly running so that our screen will persist.
run = True
# while `run` = True, run the game
while run:

  # This ticks the game's clock by the speed we set. In this case we set it to our variable `fps` which is defined above.
  clock.tick(fps)

  # display the background image on the screen.
  screen.blit(bg,(0,0))

  #draw and scroll the ground. This code here changes the code such that the image reset once it exceeds the first diagonal slash, using the timing from the clock feature to give the impression of the ground scrolling endlessly.
  screen.blit(ground_img, (ground_scroll, 768))
  ground_scroll -= scroll_speed
  if abs(ground_scroll) > 35:
    ground_scroll = 0

  # This creates the 'exit' game and allows us to close the game.
  for event in pygame.event.get():
    if event.type ==pygame.QUIT:
      run = False

  # This continuously updates the display of the screen after each loop in the while loop.
  pygame.display.update()

# exiting the while loop for `run` means we'll hit this quit() function and close the application.
pygame.quit()