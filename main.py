import pygame
from pygame.locals import *
import random

pygame.init()

# This adds timing for the game's clock (helps with the scroll speed that we set below)
clock = pygame.time.Clock()
fps = 60

# Screen dimensions
screen_width = 864
screen_height = 936

# Puts the dimensions together and displays the caption on the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)
font_color = (255, 255, 255) #white

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))


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
    if game_over == False:
      self.rect.x -= scroll_speed
      if self.rect.right < 0:
        self.kill()


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

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

  bird_group.draw(screen)
  bird_group.update()
  pipe_group.draw(screen)
  
  # draw the ground
  screen.blit(ground_img, (ground_scroll, 768))

  # Check score
  if len(pipe_group) > 0:
    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
      and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
      and pass_pipe == False:
      pass_pipe = True
    if pass_pipe == True:
      if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
        score += 1
        pass_pipe = False

  draw_text(str(score), font, font_color, int(screen_width / 2), 20)

  # look for collision
  if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
    game_over = True

  # check if bird has hit the ground
  if flappy.rect.bottom >= 768:
    game_over = True
    flying = False

  
  
  # #draw and scroll the ground. This code here changes the code such that the image reset once it exceeds the first diagonal slash, using the timing from the clock feature to give the impression of the ground scrolling endlessly.

  if game_over == False and flying == True:
    # generate new pipes
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
      pipe_height = random.randint(-100, 100)
      bottom_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
      top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
      pipe_group.add(bottom_pipe)
      pipe_group.add(top_pipe)
      last_pipe = time_now

    # ground scroll feature
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
      ground_scroll = 0

    pipe_group.update()

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