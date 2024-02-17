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

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')

# create the bird object using sprite and add the three different images.
class Bird(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.images =[]
    self.index = 0
    self.counter = 0
    for num in range(1, 4):
      img = pygame.image.load(f'img/bird{num}.png')
      self.images.append(img)
    self.image = self.images[self.index]
    self.rect = self.image.get_rect()
    self.rect.center = [x, y]

  def update(self):
    # handle the animation for the bird
    self.counter += 1
    flap_cooldown = 5
    if self.counter > flap_cooldown:
      self.counter = 0
      self.index += 1
      if self.index >= len(self.images):
        self.index = 0
    self.image =  self.images[self.index]

bird_group = pygame.sprite.Group()

# creates the placement of the object
flappy = Bird(100, int(screen_height / 2))

# makes the connection between the object and the group.
bird_group.add(flappy)


# This `run` variable should be consistantly running so that our screen will persist.
run = True
# while `run` = True, run the game
while run:

  # This ticks the game's clock by the speed we set. In this case we set it to our variable `fps` which is defined above.
  clock.tick(fps)

  # display the background image on the screen.
  screen.blit(bg,(0,0))

  # adding the bird to the game
  bird_group.draw(screen)
  bird_group.update()

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