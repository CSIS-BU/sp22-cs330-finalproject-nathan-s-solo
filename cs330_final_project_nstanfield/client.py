import socket
import pygame, sys, os
import threading

pygame.init()

BUFFER_SIZE = 2048
# server_port = input("Enter port number: ")
# server_port = int(server_port)
server_port = 6728
host = "127.0.0.1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, server_port))


WIDTH = 800
HEIGHT = 600
LINE_SIZE = 6
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
BLUE = (29, 37, 153)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption('Tic Tac Toe')
player = 0
player_turn = True
game_over = False
menu = False

data = client.recv(BUFFER_SIZE)
data = data.decode()
player = int(data)
print(player)
if player == 0:
    player_turn = True
elif player == 1:
    player_turn = False

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


# color_active = (171, 248, 255)
# color_passive = (141, 194, 199)
# color = color_passive
# active = False
# base_font = pygame.font.Font(None, 32)
# user_input = ""
# input_rect = pygame.Rect(WIDTH //2, (HEIGHT // (HEIGHT // 200)), 100, 32)
# title_font = pygame.font.Font('freesansbold.ttf', 80)
# title_text = title_font.render('Tic-Tac-Toe', True, BLACK)
# title_textRect = title_text.get_rect()
# title_textRect.center = (WIDTH //2, HEIGHT // (HEIGHT // 100))

draw()
while True:
    if menu:
        screen.fill(WHITE)
        # screen.blit(title_text, title_textRect)
        # if active:
        #     color = color_active
        # else:
        #     color = color_passive
        # pygame.draw.rect(screen, color, input_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if input_rect.collidepoint(event.pos):
            #         active = True
            #     else:
            #         active = False
        pygame.display.update()
    elif not menu and game_over == False:
        if player_turn == False:
            data = client.recv(BUFFER_SIZE)
            if data:
                data = data.decode()
                print(data)
                if data == "0":
                    player = 1
                elif data == "1":
                    player = 2
                elif "|" in data:
                    data_list = data.split('|')
                    x, y, which_player = int(data_list[0]), int(data_list[1]), data_list[2]
                    grid[y][x] = which_player
                    draw()
                    game_over = win_check()
                    player_turn = True
                    pygame.display.flip()
        # player = int(data)
        # print(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn == True:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x_box = int(pos[0] // (WIDTH/3))
                y_box = int(pos[1] // (HEIGHT/3))
                if player == 0:
                    grid[y_box][x_box] = "X"
                    client.sendall(str.encode((str(x_box) + "|" + str(y_box) + "|X")))
                elif player == 1:
                    grid[y_box][x_box] = "O"
                    client.sendall(str.encode((str(x_box) + "|" + str(y_box) + "|O")))
                player_turn = False
                print(x_box, y_box)
                print(grid)
                draw()
                game_over = win_check()
                if game_over == True:
                    client.close()
        pygame.display.flip()