import sys, pygame
import time
import geo2d
from field import Field
pygame.init()

size = width, height = 800,600
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
f = Field(width, height)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    for a in f.asteroids:
        a.draw(screen)
    pygame.display.flip()
    time.sleep(0.05)
    f.update()
