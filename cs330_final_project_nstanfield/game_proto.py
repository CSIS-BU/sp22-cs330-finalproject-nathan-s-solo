import pygame, sys
import time

pygame.init()
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()