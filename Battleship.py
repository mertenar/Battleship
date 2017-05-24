from random import randint

"""
Battleship game where one or two players compete to sink the others ships! BAM
QUESTIONS/CONSIDERATIONS:
- Some functions used just to ensure user input is correct (using while/if),
is this the best way?
"""

#initial prompt to determine names and player vs comp or player vs player
print "Welcome to Python Battleship, hope you brought the big guns! \
Let's choose settings first."

def player_count():
    number_of_players = raw_input("Will there be 1 or 2 players?  ")
    if number_of_players != "1" and number_of_players != "2":
        print "You need to pick either 1 or 2 players. Try again."
        player_count()
    else:
        pass
    return number_of_players

#create a board and sample (for ship placement) for each player
class Board(object):

    def __init__(self, name, ship_amt):
        self.board = []
        self.sample_board = []
        self.name = name
        self.ship_amt = ship_amt
        self.ships = []
        self.turn_count = 0

    def place_ships(self):
        while self.ship_amt > 0:
            print "%s, time to place your next ship." % self.name
            ship_row = raw_input("Which row will the ship go? (1-5)  ")
            try:
                ship_row = int(ship_row)
            except ValueError:
                print "Invalid number, try again."
                self.place_ships()
            if ship_row in range(1, 6):
                pass
            else:
                print "Not a valid row number, try again."
                self.place_ships()
            ship_col = raw_input("Which col will the ship go? (1-5)  ")
            try:
                ship_col = int(ship_col)
            except ValueError:
                print "Not a valid column, try placing your ship again."
                self.place_ships()
            if ship_col in range(1, 6):
                pass
            else:
                print "Not a valid column number, try placing your ship again."
                self.place_ships()
            self.ship_amt -= 1
            self.ships.append([ship_row, ship_col])
            self.sample_board[(ship_row - 1)][(ship_col - 1)] = "A"
            print "Ship added:"
            print_board(self.sample_board, self.name)
        else:
            print "%s all ships placed." % self.name

    def bot_place_ships(self):
        while self.ship_amt > 0:
            ship_row = randint(1, 5)
            ship_col = randint(1, 5)
            self.ships.append([ship_row, ship_col])
            self.ship_amt -= 1
        print "%s's ships have been placed" % self.name

def ship_amount():
    ship_amt = raw_input("How many ships would you like each player to have?\
(up to 3)  ")
    try:
        ship_amt = int(ship_amt)
        if ship_amt <= 3 and ship_amt > 0:
            print "Okay, you will each have %d ships." % ship_amt
        else:
            print "Sorry you were supposed to pick between 1 and 3. Let's try that again."
            ship_amount()
    except ValueError:
        print "Sorry you were supposed to pick between 1 and 3. Let's try that again."
        ship_amount()
    return ship_amt

def create_board(board):
    for spot in range(0, 5):
        board.append(["O"] * 5)

def print_board(board, player_name):
    j = "  "
    print player_name + "\'s board"
    for row in board:
        print j.join(row)
    print "\n"

def turn(player, opponent):
    print "%s's turn." % player.name
    print_board(opponent.board, opponent.name)
    guess_row = raw_input("Which row do you guess?  ")
    try:
        guess_row = int(guess_row)
    except ValueError:
        print "Not a valid row, try picking again."
    if guess_row in range(1, 6):
        pass
    else:
        print "Not a valid row number, try again."
        turn(player, opponent)
    guess_col = raw_input("Which column do you guess?  ")
    try:
        guess_col = int(guess_col)
    except ValueError:
        print "Not a valid column, try picking again."
    if guess_col in range(1, 6):
        pass
    else:
        print "Not a valid col number, try again."
        turn(player, opponent)
    print "You guess: %d, %d" % (guess_row, guess_col)
    if [guess_row, guess_col] in opponent.ships:
        print "Nice! You sunk a ship!"
        opponent.ships.remove([guess_row, guess_col])
        opponent.board[(guess_row - 1)][(guess_col - 1)] = "X"
    elif opponent.board[(guess_row - 1)][(guess_col - 1)] != "O":
        if opponent.board[(guess_row - 1)][(guess_col - 1)] == "/":
            print "You already guessed that spot."
        elif opponent.board[(guess_row - 1)][(guess_col - 1)] == "X":
            print "You already sunk a ship in that spot."
        print "Try again."
        turn(player, opponent)
    else:
        print "You missed."
        opponent.board[(guess_row - 1)][(guess_col - 1)] = "/"
    print_board(opponent.board, opponent.name)
    player.turn_count += 1

def bot_turn(player, opponent):
    print "%s's turn." % player.name
    print_board(opponent.board, opponent.name)
    guess_row = randint(1, 5)
    guess_col = randint(1, 5)
    if opponent.board[(guess_row - 1)][(guess_col - 1)] != "O":
        bot_turn()
    elif [guess_row, guess_col] in opponent.ships:
        print "%s guesses: %d, %d" % (player.name, guess_row, guess_col)
        print "Uh oh! The Captain sunk a ship!"
        opponent.ships.remove([guess_row, guess_col])
        opponent.board[(guess_row - 1)][(guess_col - 1)] = "X"
    else:
        print "%s guesses: %d, %d" % (player.name, guess_row, guess_col)
        print "Whew, he missed."
        opponent.board[(guess_row - 1)][(guess_col - 1)] = "/"
    print_board(opponent.board, opponent.name)
    player.turn_count += 1

#engine alternates turns using turn function until a player runs out of ships
def engine():
    while len(Player1.ships) > 0 and len(Player2.ships) > 0:
        if Player1.turn_count == Player2.turn_count:
            turn(Player1, Player2)
        else:
            if Player2.name == "Captain CruiseBot":
                bot_turn(Player2, Player1)
            else:
                turn(Player2, Player1)
    if len(Player2.ships) == 0:
        print "%s wins! Congratulations!" % Player1.name
        quit()
    else:
        if Player2.name == "Captain CruiseBot":
            print "And Captain CruiseBot is victorious again!"
        else:
            print "%s wins! Congratulations!" % Player2.name
        quit()


players = player_count()
player1_name = raw_input("Player 1 name =  ")

#if 1 player then bot is assigned, 2 players then player 2 picks name
if players == "1":
    print "Welcome %s. You will be playing against Capt CruiseBot, \
good luck!" % player1_name
    player2_name = "Captain CruiseBot"
else:
    player2_name = raw_input("Player 2 name =  ")
    print "Welcome %s and %s. Enjoy the water!" % (player1_name, player2_name)

ships = ship_amount()

#initialize player boards
Player1 = Board(player1_name, ships)
Player2 = Board(player2_name, ships)

#create starting boards
create_board(Player1.board)
create_board(Player1.sample_board)
create_board(Player2.board)
create_board(Player2.sample_board)

#show initial boards
print_board(Player1.board, Player1.name)
print_board(Player2.board, Player2.name)

#place ships, bot goes to auto select
Player1.place_ships()
if Player2.name == "Captain CruiseBot":
    Player2.bot_place_ships()
else:
    Player2.place_ships()

engine()
