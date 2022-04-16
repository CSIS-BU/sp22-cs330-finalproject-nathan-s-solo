import pygame, sys
import time

pygame.init()
WIDTH = 800
HEIGHT = 600
LINE_SIZE = 6
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption('Game')

def create_grid():
    pygame.draw.line(screen, BLACK, (WIDTH/3, 0), (WIDTH/3,HEIGHT), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (0, HEIGHT/3), (WIDTH,HEIGHT/3), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (WIDTH/1.5, 0), (WIDTH/1.5,HEIGHT), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (0, HEIGHT/1.5), (WIDTH,HEIGHT/1.5), LINE_SIZE)

create_grid()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                print(pos)

    pygame.display.update()