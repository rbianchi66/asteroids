import sys, pygame
import time
import geo2d
from asteroid import Asteroid
from trajectory import Trajectory
pygame.init()

size = width, height = 800,600
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
objects = [
            Asteroid(50, Trajectory(geo2d.P(100,10), geo2d.P(1000, 1000))),
            Asteroid(90, Trajectory(geo2d.P(200,600), geo2d.P(1000, 0))),
           ]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    for o in objects:
        o.draw(screen)
    pygame.display.flip()
    time.sleep(0.05)
    for o in objects:
        o.updatePos()
