
# Changelog
## 4/25/22
  * added main menu
  * added input menu to input ip and port info
  * added some input validation for the input menu
  * added status update during game to give the player information about the game state
  * added game logic to handle a tie
  * added return to menu button once the game has ended to allow players to play again
  * added the server being able to handle multiple games in one session without needing to restart
  * smoothed out and fixed bugs with the simultaneous client connection
## 4/23/22
  * added server accepting multiple clients at the same time with multithreading
  * added each player taking turns and their moves being reflected in both client programs
## 4/20/22
  * added base code for socket programming for client and server code
## 4/18/22
  * added a line to visually show the winning 3 squares
  * the game stops after a winner is detected
## 4/16/22
  * added backend grid to keep track of values
  * added ability to click on grid to place an X or O in that space depending on player value
  * added win_check function that has game logic to determine if player 1 or 2 wins
  * added image files for x and o
