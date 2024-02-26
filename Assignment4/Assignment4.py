import sys


# count = total number of the given type of ship
# symbol = initial letter of the ship
class Ship:
    def __init__(self, count, symbol, length):
        self.count = count
        self.symbol = symbol
        self.length = length


# defining ships
carrier = Ship(1, "C", 5)
battle_ship = Ship(2, "B", 4)
destroyer = Ship(1, "D", 3)
submarine = Ship(1, "S", 3)
patrol_boat = Ship(4, "P", 2)


# ships = ship layout of player
# opt_ships = positions of battleship and patrol boat
# board = hidden board
# moves = a list contains players moves
class Player:
    def __init__(self, ships, opt_ships, board, moves):
        self.ships = ships
        self.opt_ships = opt_ships
        self.board = board
        self.moves = moves


def output_function(out):
    print(out, end="")
    outfile.write(out)


# places ships according to positions at player1-2.txt and optionalplayer1-2.txt
# this function returns ship layout and battleship, patrol boat positions at ship layout
def place_ships(file_name, opt_file):
    player_lines = file_name.read().splitlines()
    player = [item.split(";") for item in player_lines]

    # check if the ship symbols are correctly given
    for list1 in player:
        for element in list1:
            if element.isalpha():
                if element not in ["C", "B", "D", "S", "P"]:
                    raise Exception

    # controls ship number in txt files
    def count_letter(ship):
        count = sum(1 if element == ship.symbol else 0 for lis1 in player for element in lis1)
        return count == ship.length * ship.count

    for element in [carrier, battle_ship, destroyer, submarine, patrol_boat]:
        if count_letter(element):
            pass
        else:
            raise Exception

    player_ships = [["-" if ele == "" else ele.upper() for ele in j] for count, j in enumerate(player)]

    b_list = []
    p_list = []
    with open(opt_file) as opt:
        optlines = opt.read().splitlines()
    for line in optlines:
        pure = line.rstrip(";")
        ship_info = pure[3:].split(";")
        index_x = int(ship_info[0].split(",")[0])
        index_y = ship_info[0].split(",")[1]
        alp_index = alphabet.index(index_y)

        if pure[0] == "B":
            if ship_info[1] == "right":
                b_list.append([(index_x, alphabet[alp_index]), (index_x, alphabet[alp_index+1]), (index_x, alphabet[alp_index+2]), (index_x, alphabet[alp_index+3])])
            elif ship_info[1] == "down":
                b_list.append([(index_x, alphabet[alp_index]), (index_x+1, alphabet[alp_index]), (index_x+2, alphabet[alp_index]), (index_x+3, alphabet[alp_index])])

        elif pure[0] == "P":
            if ship_info[1] == "right":
                p_list.append([(index_x, alphabet[alp_index]), (index_x, alphabet[alp_index+1])])
            elif ship_info[1] == "down":
                p_list.append([(index_x, alphabet[alp_index]), (index_x+1, alphabet[alp_index])])
    hard_ones = [b_list, p_list]

    return player_ships, hard_ones


# splits players move and checks its correctness according to game rules
# checks if the square that the player hit is empty or not at ship layout
# then changes that position to "X" or "O" at hidden board
def move_player(player, enemy, index):

    if "," not in player.moves[index] or len(player.moves[index]) == 0 or player.moves[index].split(",")[0] == "" or player.moves[index].split(",")[1] == "" :
        raise IndexError(f"IndexError: Missing index at move '{player.moves[index]}'.")

    if player.moves[index].split(",")[1].isalpha() is False or player.moves[index].split(",")[0].isdigit() is False or len(player.moves[index]) > 4:
        raise ValueError(f"ValueError: '{player.moves[index]}' is not a valid move.")

    player_x, player_y = int(player.moves[index].split(",")[0]), player.moves[index].split(",")[1]

    assert 1 <= int(player.moves[index].split(",")[0]) <= 10 and player.moves[index].split(",")[1] in alphabet, "AssertionError: Invalid Operation."

    column = alphabet.index(player.moves[index].split(",")[1])

    assert not enemy.board[player_x - 1][column].isalpha(), "AssertionError: Invalid Operation."

    if enemy.ships[player_x-1][column].isalpha():
        enemy.board[player_x-1][column] = "X"
    else:
        enemy.board[player_x-1][column] = "O"


# identifies positions of wanted ship type and counts ships that are left in game
# returns the symbolic expression of sunken and left ships to print to user
# returns number of ships left in the game to declare the winner in other functions
def count_ships(ship_type, player):
    # getting "X" positions in hidden boards
    board = []
    for count, row in enumerate(player.board):
        for i in range(len(row)):
            if row[i] == "X":
                board.append((count+1, alphabet[i]))

    # Battleships' positions
    if ship_type.symbol == "B":
        liste = []
        for items in player.opt_ships:
            for item in items:
                if len(item) == 4:
                    liste.append(item)

    # Patrol Boats' positions
    elif ship_type.symbol == "P":
        liste = []
        for items in player.opt_ships:
            for item in items:
                if len(item) == 2:
                    liste.append(item)

    # submarine, carrier and destroyer ships positions
    else:
        liste = []
        for count, row in enumerate(player.ships):
            for i in range(10):
                if row[i] == ship_type.symbol:
                    liste.append((count+1, alphabet[i]))
        liste = [liste]

    # counting sunk ships
    c = 0
    for items in liste:
        if set(items).issubset(set(board)):
            c += 1
    return ship_type.count-c, "X"*c+"-"*(ship_type.count-c)  # number of remaining ships and their symbol for printing purposes


# prints game layout to user
def write_moves(player, index, round):
    ship_str = f"Carrier\t\t{' '.join(count_ships(carrier, player1)[1])}\t\t\t\tCarrier\t\t{' '.join(count_ships(carrier, player2)[1])}\n" \
        f"Battleship\t{' '.join(count_ships(battle_ship, player1)[1])}\t\t\t\tBattleship\t{' '.join(count_ships(battle_ship, player2)[1])}\n" \
        f"Destroyer\t{' '.join(count_ships(destroyer, player1)[1])}\t\t\t\tDestroyer\t{' '.join(count_ships(destroyer, player2)[1])}\n" \
        f"Submarine\t{' '.join(count_ships(submarine, player1)[1])}\t\t\t\tSubmarine\t{' '.join(count_ships(submarine, player2)[1])}\n" \
        f"Patrol Boat\t{' '.join(count_ships(patrol_boat, player1)[1])}\t\t\tPatrol Boat\t{' '.join(count_ships(patrol_boat, player2)[1])}\n"

    output_function(f"\n{'Player1' if player == player1 else 'Player2'}'s Move\n\n")
    output_function(f"Round : {round}\t\t\t\t\tGrid Size: 10x10\n\n")
    output_function("Player1's Hidden Board\t\tPlayer2's Hidden Board\n")
    output_function(f"  {' '.join(alphabet)}\t\t  {' '.join(alphabet)}\n")
    for j in range(10):
        output_function(f"{str(j + 1) : <2}{' '.join(player1.board[j])}\t\t{str(j + 1) : <2}{' '.join(player2.board[j])}\n")
    output_function("\n")
    output_function(ship_str)
    output_function(f"\nEnter your move: {player.moves[index]}\n")


# prints final version of board and the result of the game to user
def final_write():
    ship_str = f"Carrier\t\t{' '.join(count_ships(carrier, player1)[1])}\t\t\t\tCarrier\t\t{' '.join(count_ships(carrier, player2)[1])}\n" \
               f"Battleship\t{' '.join(count_ships(battle_ship, player1)[1])}\t\t\t\tBattleship\t{' '.join(count_ships(battle_ship, player2)[1])}\n" \
               f"Destroyer\t{' '.join(count_ships(destroyer, player1)[1])}\t\t\t\tDestroyer\t{' '.join(count_ships(destroyer, player2)[1])}\n" \
               f"Submarine\t{' '.join(count_ships(submarine, player1)[1])}\t\t\t\tSubmarine\t{' '.join(count_ships(submarine, player2)[1])}\n" \
               f"Patrol Boat\t{' '.join(count_ships(patrol_boat, player1)[1])}\t\t\tPatrol Boat\t{' '.join(count_ships(patrol_boat, player2)[1])}\n"

    output_function(f"\n{game_over()[0]}")
    output_function("Final Information\n\n")
    output_function("Player1's Board\t\t\t\tPlayer2's Board\n")
    output_function(f"  {' '.join(alphabet)}\t\t  {' '.join(alphabet)}\n")
    for j in range(10):
        output_function(
            f"{str(j + 1) : <2}{' '.join(rem_ships(player1)[j])}\t\t{str(j + 1) : <2}{' '.join(rem_ships(player2)[j])}\n")
    output_function("\n")
    output_function(ship_str)


# checks if the game is going to continue or not
# uses count_ships() function
def game_over():
    a = count_ships(carrier, player1)[0] + count_ships(battle_ship, player1)[0] + count_ships(destroyer, player1)[0] + count_ships(submarine, player1)[0] + count_ships(patrol_boat, player1)[0]
    b = count_ships(carrier, player2)[0] + count_ships(battle_ship, player2)[0] + count_ships(destroyer, player2)[0] + count_ships(submarine, player2)[0] + count_ships(patrol_boat, player2)[0]
    if a == 0 and b == 0:
        return "It is a Draw!\n\n", True
    elif a == 0:
        return "Player2 Wins!\n\n", True
    elif b == 0:
        return "Player1 Wins!\n\n", True
    else:
        return None, False


# returns the final information board with left ships symbols
def rem_ships(player):
    liste = []
    for count, row in enumerate(player.ships):
        for i in range(len(row)):
            if row[i].isalpha():
                liste.append([count, i])

    for item in liste:
        if player.board[item[0]][item[1]].isalpha():
            pass
        else:
            player.board[item[0]][item[1]] = player.ships[item[0]][item[1]]

    return player.board


# main part of the program
alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
hidden_board1 = [["-" for i in range(10)] for j in range(10)]
hidden_board2 = [["-" for k in range(10)] for m in range(10)]

outfile = open("Battleship.out", "w")

# check if the files exist
file = []
for ele in sys.argv[1:5]:
    try:
        open(ele, "r")
    except IOError:
        file.append(ele)


if file:
    output_function(f"IOError: input file(s) {', '.join(file)} is/are not reachable.\n")
    exit()
else:
    try:
        player1_txt, player2_txt = open(sys.argv[1], "r"), open(sys.argv[2], "r")
        player1_in, player2_in = open(sys.argv[3], "r"), open(sys.argv[4], "r")
    except IndexError:
        output_function("IndexError: Missing Argument")
        exit()

    try:
        player1_moves = player1_in.read().rstrip(";").split(";")
        player2_moves = player2_in.read().rstrip(";").split(";")

        act_ships1, opt_ships1 = place_ships(player1_txt, "OptionalPlayer1.txt")
        act_ships2, opt_ships2 = place_ships(player2_txt, "OptionalPlayer2.txt")

        player1 = Player(act_ships1, opt_ships1, hidden_board1, player1_moves)
        player2 = Player(act_ships2, opt_ships2, hidden_board2, player2_moves)

        output_function("Battle of Ships Game\n\n")

        ship_str = f"Carrier\t\t{' '.join(count_ships(carrier, player1)[1])}\t\t\t\tCarrier\t\t{' '.join(count_ships(carrier, player2)[1])}\n" \
                   f"Battleship\t{' '.join(count_ships(battle_ship, player1)[1])}\t\t\t\tBattleship\t{' '.join(count_ships(battle_ship, player2)[1])}\n" \
                   f"Destroyer\t{' '.join(count_ships(destroyer, player1)[1])}\t\t\t\tDestroyer\t{' '.join(count_ships(destroyer, player2)[1])}\n" \
                   f"Submarine\t{' '.join(count_ships(submarine, player1)[1])}\t\t\t\tSubmarine\t{' '.join(count_ships(submarine, player2)[1])}\n" \
                   f"Patrol Boat\t{' '.join(count_ships(patrol_boat, player1)[1])}\t\t\tPatrol Boat\t{' '.join(count_ships(patrol_boat, player2)[1])}\n"

        output_function(f"Player1's Move\n\n")
        output_function(f"Round : {1}\t\t\t\t\tGrid Size: 10x10\n\n")
        output_function("Player1's Hidden Board\t\tPlayer2's Hidden Board\n")
        output_function(f"  {' '.join(alphabet)}\t\t  {' '.join(alphabet)}\n")
        for j in range(10):
            output_function(
                f"{str(j + 1) : <2}{' '.join(player1.board[j])}\t\t{str(j + 1) : <2}{' '.join(player2.board[j])}\n")
        output_function("\n")
        output_function(ship_str)
        output_function(f"\nEnter your move: {player1.moves[0]}\n")

        i, j = 0, 0
        round = 1
        while i < len(player1.moves):
            try:
                move_player(player1, player2, i)
            except (IndexError, ValueError, AssertionError) as e:
                output_function(f"{e}\n")
                output_function(f"Enter your move: {player1.moves[i+1]}\n")
                i += 1
                continue
            else:
                i += 1

            write_moves(player2, j, round)
            while j < len(player2.moves):
                try:
                    move_player(player2, player1, j)
                except (IndexError, ValueError, AssertionError) as e:
                    output_function(f"{e}\n")
                    output_function(f"Enter your move: {player2.moves[j+1]}\n")
                    j += 1
                    continue
                else:
                    round += 1
                    j += 1
                    break

            if game_over()[1]:
                final_write()
                break
            else:
                write_moves(player1, i, round)

    except Exception:
        output_function("kaBOOM: run for your life!\n")
        exit()

# Ezgi EKİN
# 2210356029
