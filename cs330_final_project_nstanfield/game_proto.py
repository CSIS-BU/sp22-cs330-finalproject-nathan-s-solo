
import pygame, sys, os

pygame.init()

WIDTH = 800
HEIGHT = 600
LINE_SIZE = 6
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
BLUE = (29, 37, 153)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption('Game')
player = 1
player_turn = True
game_over = False

raw_letter_x = pygame.image.load(os.path.join("images", "x_image.png"))
letter_x = pygame.transform.scale(raw_letter_x, (((WIDTH/3) - 15), ((HEIGHT/3) - 15)))
raw_letter_o = pygame.image.load(os.path.join("images", "o_image.png"))
letter_o = pygame.transform.scale(raw_letter_o, (((WIDTH/3) - 15), ((HEIGHT/3) - 15)))

grid = [[0 for x in range(3)] for y in range(3)]

def draw():
    pygame.draw.line(screen, BLACK, (WIDTH/3, 0), (WIDTH/3,HEIGHT), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (0, HEIGHT/3), (WIDTH,HEIGHT/3), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (WIDTH/1.5, 0), (WIDTH/1.5,HEIGHT), LINE_SIZE)
    pygame.draw.line(screen, BLACK, (0, HEIGHT/1.5), (WIDTH,HEIGHT/1.5), LINE_SIZE)

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "X":
                screen.blit(letter_x, ((x*(WIDTH/3)) + WIDTH/100, (y*(HEIGHT/3)) + HEIGHT/100))
            elif grid[y][x] == "O":
                screen.blit(letter_o, ((x*(WIDTH/3)) + WIDTH/100, (y*(HEIGHT/3))+ HEIGHT/100))

def draw_win_line(start_space, end_space):
    x1 = start_space[0] * (WIDTH/3)
    x1 = x1 + ((WIDTH/3)/2)
    y1 = start_space[1] * (HEIGHT/3)
    y1 = y1 + ((HEIGHT/3)/2)
    x2 = end_space[0] * (WIDTH/3)
    x2 = x2 + ((WIDTH/3)/2)
    y2 = end_space[1] * (HEIGHT/3)
    y2 = y2 + ((HEIGHT/3)/2)
    pygame.draw.line(screen, BLUE, (x1, y1), (x2,y2), LINE_SIZE)

def win_check():

    if grid[2][0] == "X" and grid[1][1] == "X" and grid[0][2] == "X":
        draw_win_line((2,0),(0,2))
        return True
    elif grid[2][0] == "O" and grid[1][1] == "O" and grid[0][2] == "O":
        draw_win_line((2,0),(0,2))
        return True
    if grid[0][0] == "X" and grid[1][1] == "X" and grid[2][2] == "X":
        draw_win_line((0,0),(2,2))
        return True
    elif grid[0][0] == "O" and grid[1][1] == "O" and grid[2][2] == "O":
        draw_win_line((0,0),(2,2))
        return True

    for i in range(len(grid)):
        if grid[0][i] == "X" and grid[1][i] == "X" and grid[2][i] == "X":
            draw_win_line((i,0),(i,2))
            return True
        elif grid[0][i] == "O" and grid[1][i] == "O" and grid[2][i] == "O":
            draw_win_line((i,0),(i,2))
            return True
        if grid[i][0] == "X" and grid[i][1] == "X" and grid[i][2] == "X":
            draw_win_line((0,i),(2,i))
            return True
        elif grid[i][0] == "O" and grid[i][1] == "O" and grid[i][2] == "O":
            draw_win_line((0,i),(2,i))
            return True
    return False



draw()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x_box = int(pos[0] // (WIDTH/3))
                y_box = int(pos[1] // (HEIGHT/3))
                if player == 1:
                    grid[y_box][x_box] = "X"
                elif player == 2:
                    grid[y_box][x_box] = "O"
                print(x_box, y_box)
                print(grid)
                draw()
                game_over = win_check()
        pygame.display.update()