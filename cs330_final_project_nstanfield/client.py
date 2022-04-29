from re import L
import socket
import pygame, sys, os
import threading

#initalize variables
pygame.init()

BUFFER_SIZE = 2048

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
menu = True
main_menu = True
input_menu = False
invalid_input = False
socket_error = False


raw_letter_x = pygame.image.load(os.path.join("images", "x_image.png"))
letter_x = pygame.transform.scale(raw_letter_x, (((WIDTH/3) - 15), ((HEIGHT/3) - 15)))
raw_letter_o = pygame.image.load(os.path.join("images", "o_image.png"))
letter_o = pygame.transform.scale(raw_letter_o, (((WIDTH/3) - 15), ((HEIGHT/3) - 15)))

grid = [[0 for x in range(3)] for y in range(3)]

#function to render the grid and grid values
def draw():
    screen.fill(WHITE)
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

#function to draw a line through the winning 3 spaces
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

#function to create status texts so the player know the current game state
def status_text(update_text):
    pygame.draw.rect(screen, (38, 44, 66), (0, 578, 210, 45))
    update_font = pygame.font.Font('freesansbold.ttf', 12)
    updated_text = update_font.render(update_text, True, WHITE)
    updated_textRect = updated_text.get_rect()
    updated_textRect.center = (105, 590)
    screen.blit(updated_text, updated_textRect)
    pygame.display.flip()

#game logic to determine a winner
def win_check():

    if grid[2][0] == "X" and grid[1][1] == "X" and grid[0][2] == "X":
        draw_win_line((2,0),(0,2))
        status_text("X wins!")
        return True
    elif grid[2][0] == "O" and grid[1][1] == "O" and grid[0][2] == "O":
        draw_win_line((2,0),(0,2))
        status_text("O wins!")
        return True
    if grid[0][0] == "X" and grid[1][1] == "X" and grid[2][2] == "X":
        draw_win_line((0,0),(2,2))
        status_text("X wins!")
        return True
    elif grid[0][0] == "O" and grid[1][1] == "O" and grid[2][2] == "O":
        draw_win_line((0,0),(2,2))
        status_text("O wins!")
        return True

    counter = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X" or grid[i][j] == "O":
                counter += 1
        if grid[0][i] == "X" and grid[1][i] == "X" and grid[2][i] == "X":
            draw_win_line((i,0),(i,2))
            status_text("X wins!")
            return True
        elif grid[0][i] == "O" and grid[1][i] == "O" and grid[2][i] == "O":
            draw_win_line((i,0),(i,2))
            status_text("O wins!")
            return True
        if grid[i][0] == "X" and grid[i][1] == "X" and grid[i][2] == "X":
            draw_win_line((0,i),(2,i))
            status_text("X wins!")
            return True
        elif grid[i][0] == "O" and grid[i][1] == "O" and grid[i][2] == "O":
            draw_win_line((0,i),(2,i))
            status_text("O wins!")
            return True
    if counter == (len(grid) * len(grid[i])):
        status_text("Game is a Tie!")
        return True
    return False

#function to create an error message on the input screen
def input_error(text):
    inputerror_font = pygame.font.Font('freesansbold.ttf', 24)
    inputerror_text = inputerror_font.render(text, True, (217, 78, 78))
    inputerror_textRect = inputerror_text.get_rect()
    inputerror_textRect.center = ((WIDTH //2), HEIGHT // (HEIGHT / 350))
    screen.blit(inputerror_text, inputerror_textRect)

#function to run in a thread so the client who is waiting for their turn can receive data without the client window freezing
def wait_for_data():
    global player, player_turn, game_over
    data = client.recv(BUFFER_SIZE).decode()
    if data:
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
            if game_over == True:
                client.sendall(str.encode("GAMEOVER"))
                client.close()
                draw()
                win_check()
                return
            player_turn = True
            pygame.display.flip()
    return

# main menu UI
def render_title():
    title_font = pygame.font.Font('freesansbold.ttf', 80)
    title_text = title_font.render('Tic-Tac-Toe', True, BLACK)
    title_textRect = title_text.get_rect()
    title_textRect.center = (WIDTH //2, HEIGHT // (HEIGHT // 115))
    screen.blit(title_text, title_textRect)

play_rect = pygame.Rect(((WIDTH // 2) - 60, HEIGHT // 1.8, 120, 45))
credit_font = pygame.font.Font('freesansbold.ttf', 24)
credit_text = credit_font.render('By Nathan Stanfield', True, BLACK)
credit_textRect = credit_text.get_rect()
credit_textRect.center = (WIDTH //2, HEIGHT // (HEIGHT // 151))
play_font = pygame.font.SysFont('freesansbold.ttf', 40)
play_text = play_font.render("Play", 1, (237, 237, 237))
play_textRect = play_text.get_rect()
play_textRect.center = (WIDTH //2, (HEIGHT // 1.8) + 22)

#input text for ip and port
font = pygame.font.Font(None, 32)
input_desc_text = font.render('Input IP and Port (format IP|Port) example: 127.0.0.1|6728', True, BLACK)
input_desc_textRect = credit_text.get_rect()
input_desc_textRect.center = ((WIDTH //2) - 150, HEIGHT // (HEIGHT / 280))
input_box = pygame.Rect((WIDTH // 2) - 125, HEIGHT // 2, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

draw()
while True:
    if menu and game_over == False:
        #render main menu visuals
        if main_menu:
            screen.fill(WHITE)
            play_button_rect = pygame.Rect(((WIDTH // 2) - 60, HEIGHT // 1.8, 120, 45))
            pygame.draw.rect(screen, (103, 114, 163), play_rect)
            pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(pos):
                pygame.draw.rect(screen, (102, 122, 212), play_rect)
            render_title()
            screen.blit(play_text, play_textRect)
            screen.blit(credit_text, credit_textRect)
        #render input menu visuals
        elif input_menu:
            screen.fill(WHITE)
            render_title()
            screen.blit(input_desc_text, input_desc_textRect)
            txt_surface = font.render(text, True, color)
            width = max(250, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen, color, input_box, 2)
            if invalid_input:
                input_error("Invalid Input")
            elif socket_error:
                input_error("Socket Connection Error")
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #if the play button is pressed go to the input meny
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if play_button_rect.collidepoint(event.pos):
                        input_menu = True
                        main_menu = False
                        screen.fill(WHITE)
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
            #determines text input from user and displays it in the input box. also reads input to connect to socket
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if "|" in text:
                            text_list = text.split('|')
                            host, server_port = (text_list[0]), (text_list[1])
                            if server_port.isnumeric():
                                invalid_input = False
                                server_port = int(server_port)
                                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                try:
                                    client.connect((host, server_port))
                                except:
                                    print("Socket Connection Failed")
                                    text = ''
                                    socket_error = True
                                    break
                                draw()
                                status_text("Waiting for Opponent")
                                pygame.display.flip()
                                data = client.recv(BUFFER_SIZE)
                                data = data.decode()
                                player = int(data)
                                if player == 0:
                                    player_turn = True
                                elif player == 1:
                                    player_turn = False
                                thread = threading.Thread(target=wait_for_data, args=())
                                thread.daemon = True
                                thread.start()
                                menu = False
                                input_menu = False
                                invalid_input = False
                                socket_error = False
                                main_menu = True
                                text = ''
                            else:
                                invalid_input = True
                                text = ''
                        else:
                            invalid_input = True
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 30:
                            text += event.unicode
        pygame.display.flip()
    #detects clicks and updates the grid values and sends the coordinate data to the server
    elif not menu and game_over == False:
        if player_turn == True:
            status_text("Your Turn")
        elif player_turn == False:
            status_text("Opponent's Turn")
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
                    draw()
                    game_over = win_check()
                    thread = threading.Thread(target=wait_for_data, args=())
                    thread.daemon = True
                    thread.start()
                    if game_over == True:
                        client.sendall(str.encode("GAMEOVER"))
                        client.close()
                        draw()
                        win_check()
        pygame.display.flip()
    #renders return to menu button and resets game once it is over
    if not menu and game_over == True:
        return_text = play_font.render("Return to Menu", 1, (237, 237, 237))
        return_textRect = return_text.get_rect()
        return_textRect.center = ((WIDTH //2), HEIGHT // (HEIGHT / 330))
        return_rect = pygame.Rect(((WIDTH // 2) - 150, HEIGHT // 2, 300, 60))
        return_button_rect = pygame.Rect(((WIDTH // 2) - 150, HEIGHT // 2, 300, 60))
        pygame.draw.rect(screen, (103, 114, 163), return_rect)
        pos = pygame.mouse.get_pos()
        if return_button_rect.collidepoint(pos):
            pygame.draw.rect(screen, (102, 122, 212), return_rect)
        screen.blit(return_text, return_textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if play_button_rect.collidepoint(event.pos):
                        menu = True
                        game_over = False
                        screen.fill(WHITE)
                        grid = [[0 for x in range(3)] for y in range(3)]
        pygame.display.flip()