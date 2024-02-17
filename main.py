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
fps = 60

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150

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
    self.vel = 0
    self.clicked = False

  def update(self):

    # gravity
    if flying == True:
      self.vel += 0.5
      if self.vel > 8:
        self.vel = 8
      if self.rect.bottom < 768:
        self.rect.y += int(self.vel)

    if game_over == False:
      # jump
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        self.vel = -10
      if pygame.mouse.get_pressed()[0] == 0:
        self.clicked = False

      # handle the animation for the bird
      self.counter += 1
      flap_cooldown = 5
      if self.counter > flap_cooldown:
        self.counter = 0
        self.index += 1
        if self.index >= len(self.images):
          self.index = 0
      self.image =  self.images[self.index]

      # rotate the bird
      self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
    else:
      self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
  def __init__(self, x, y, position):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/pipe.png')
    self.rect = self.image.get_rect()
    # position 1 is from the top, -1 is from the bottom
    if position == 1:
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect.bottomleft = [x, y - (int(pipe_gap / 2))]
    if position == -1:
      self.rect.topleft = [x, y + (int(pipe_gap / 2))]

  def update(self):
    self.rect.x -= scroll_speed

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# creates the placement of the object
flappy = Bird(100, int(screen_height / 2))

# makes the connection between the object and the group.
bird_group.add(flappy)

bottom_pipe = Pipe(300, int(screen_height / 2), -1)
top_pipe = Pipe(300, int(screen_height / 2), 1)

pipe_group.add(bottom_pipe)
pipe_group.add(top_pipe)


# This `run` variable should be consistantly running so that our screen will persist.
run = True
# while `run` = True, run the game
while run:

  # This ticks the game's clock by the speed we set. In this case we set it to our variable `fps` which is defined above.
  clock.tick(fps)

  # display the background image on the screen.
  screen.blit(bg,(0,0))

  # check if bird has hit the ground
  if flappy.rect.bottom > 768:
    game_over = True
    flying = False

  # adding the bird to the game
  bird_group.draw(screen)
  bird_group.update()
  pipe_group.draw(screen)
  pipe_group.update()

  # draw the ground
  screen.blit(ground_img, (ground_scroll, 768))

  #draw and scroll the ground. This code here changes the code such that the image reset once it exceeds the first diagonal slash, using the timing from the clock feature to give the impression of the ground scrolling endlessly.

  if game_over == False:
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
      ground_scroll = 0

  # This creates the 'exit' game and allows us to close the game.
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
    if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
      flying = True

  # This continuously updates the display of the screen after each loop in the while loop.
  pygame.display.update()

# exiting the while loop for `run` means we'll hit this quit() function and close the application.
pygame.quit()