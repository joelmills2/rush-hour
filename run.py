from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from boards import all_boards
import random
import os
from colorama import Back, Style, Fore
from nnf import config

config.sat_backend = "kissat"

# Grid dimensions
GRID_SIZE = 6


prev_colour_board = [[]]


colour_mapping = {
    10: "Light Green",
    11: "Light Yellow",
    12: "Blue",
    202: "Orange",
    129: "Purple",
    43: "Cyan",
    163: "Magenta",
    22: "Dark Green",
    17: "Navy",
    6: "Teal",
    1: "Maroon",
    8: "Grey",
    15: "White",
    138: "Pinkish Brown",
    178: "Gold",
    88: "Dark Red",
}

# Helper function to assign colours to H2, H3, V2, and V3 pairs
selected_colours = [
    (num, colour_mapping[num])
    for num in [
        10,
        11,
        12,
        202,
        129,
        43,
        163,
        22,
        17,
        6,
        1,
        8,
        15,
        138,
        178,
        88,
    ]
]


def clear_screen():
    """
    Clears the console screen.

    This function is used to refresh the game display by clearing the existing content
    from the console. It ensures that the game's visual output is clean and uncluttered.
    """
    # Clear the console screen.
    os.system("cls" if os.name == "nt" else "clear")


def initialize_encoding():
    """
    Initializes the encoding for storing game constraints.

    This function sets up the encoding environment that is used to define the rules and
    constraints of the game. It includes the creation of proposition classes for each
    type of cell content on the game board.
    """
    # Encoding that will store all of your constraints
    E = Encoding()

    # To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
    # Proposition classes for each type of cell content
    @proposition(E)
    class Empty:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"Empty({self.x},{self.y})"

    @proposition(E)
    class Red:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"Red({self.x},{self.y})"

    @proposition(E)
    class H2:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"H2({self.x},{self.y})"

    @proposition(E)
    class H3:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"H3({self.x},{self.y})"

    @proposition(E)
    class V2:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"V2({self.x},{self.y})"

    @proposition(E)
    class V3:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"V3({self.x},{self.y})"

    @proposition(E)
    class CMR:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"CMR({self.x},{self.y})"

    @proposition(E)
    class CML:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"CML({self.x},{self.y})"

    @proposition(E)
    class CMU:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"CMU({self.x},{self.y})"

    @proposition(E)
    class CMD:
        def __init__(self, x, y):
            self.x, self.y = x, y

        def __repr__(self):
            return f"CMD({self.x},{self.y})"

    return E, Empty, H2, H3, V2, V3, CMR, CML, CMU, CMD, Red


# Innitialize Empty Grid
def create_grid():
    """
    Creates an empty grid of size GRID_SIZE x GRID_SIZE.
    """
    new_grid = [[{} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return new_grid


# Fill Grid with propositions
def fill_grid(grid, Empty, H2, H3, V2, V3, CMR, CML, CMU, CMD, Red):
    """
    Fills the grid with propositions for each cell.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            grid[x][y]["E"] = Empty(x, y)
            grid[x][y]["H2"] = H2(x, y)
            grid[x][y]["H3"] = H3(x, y)
            grid[x][y]["V2"] = V2(x, y)
            grid[x][y]["V3"] = V3(x, y)
            grid[x][y]["CMR"] = CMR(x, y)
            grid[x][y]["CML"] = CML(x, y)
            grid[x][y]["CMU"] = CMU(x, y)
            grid[x][y]["CMD"] = CMD(x, y)
            if y == 2:
                grid[x][y]["Red"] = Red(x, y)
    return grid


# CONSTRAINT FUNCTIONS
def only_one_state(grid):
    """
    Ensures that each cell has only one state.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if y == 2:
                constraint.add_exactly_one(
                    E,
                    [
                        grid[x][y]["E"],
                        grid[x][y]["H2"],
                        grid[x][y]["H3"],
                        grid[x][y]["V2"],
                        grid[x][y]["V3"],
                        grid[x][y]["Red"],
                    ],
                )

            else:
                constraint.add_exactly_one(
                    E,
                    [
                        grid[x][y]["E"],
                        grid[x][y]["H2"],
                        grid[x][y]["H3"],
                        grid[x][y]["V2"],
                        grid[x][y]["V3"],
                    ],
                )


def can_move_down(x, y, grid):
    """
    Checks whether a car can move down.
    """
    E.add_constraint((grid[x][y]["V2"] & grid[x][y + 1]["E"]) >> grid[x][y]["CMD"])
    E.add_constraint((grid[x][y]["V3"] & grid[x][y + 1]["E"]) >> grid[x][y]["CMD"])
    E.add_constraint(
        grid[x][y]["CMD"]
        >> (grid[x][y + 1]["E"] & (grid[x][y]["V2"] | grid[x][y]["V3"]))
    )


def can_move_up(x, y, grid):
    """
    Checks whether a car can move up.
    """
    E.add_constraint((grid[x][y]["V2"] & grid[x][y - 1]["E"]) >> grid[x][y]["CMU"])
    E.add_constraint((grid[x][y]["V3"] & grid[x][y - 1]["E"]) >> grid[x][y]["CMU"])
    E.add_constraint(
        grid[x][y]["CMU"]
        >> (grid[x][y - 1]["E"] & (grid[x][y]["V2"] | grid[x][y]["V3"]))
    )


def can_move_right(x, y, grid):
    """
    Checks whether a car can move right.
    """
    E.add_constraint((grid[x][y]["H2"] & grid[x + 1][y]["E"]) >> grid[x][y]["CMR"])
    E.add_constraint((grid[x][y]["H3"] & grid[x + 1][y]["E"]) >> grid[x][y]["CMR"])
    if y == 2:
        E.add_constraint((grid[x][y]["Red"] & grid[x + 1][y]["E"]) >> grid[x][y]["CMR"])
        E.add_constraint(
            grid[x][y]["CMR"]
            >> (
                grid[x + 1][y]["E"]
                & (grid[x][y]["H2"] | grid[x][y]["H3"] | grid[x][y]["Red"])
            )
        )
    else:
        E.add_constraint(
            grid[x][y]["CMR"]
            >> (grid[x + 1][y]["E"] & (grid[x][y]["H2"] | grid[x][y]["H3"]))
        )


def can_move_left(x, y, grid):
    """
    Checks whether a car can move left.
    """
    E.add_constraint((grid[x][y]["H2"] & grid[x - 1][y]["E"]) >> grid[x][y]["CML"])
    E.add_constraint((grid[x][y]["H3"] & grid[x - 1][y]["E"]) >> grid[x][y]["CML"])
    if y == 2:
        E.add_constraint((grid[x][y]["Red"] & grid[x - 1][y]["E"]) >> grid[x][y]["CML"])
        E.add_constraint(
            grid[x][y]["CML"]
            >> (
                grid[x - 1][y]["E"]
                & (grid[x][y]["H2"] | grid[x][y]["H3"] | grid[x][y]["Red"])
            )
        )
    else:
        E.add_constraint(
            grid[x][y]["CML"]
            >> (grid[x - 1][y]["E"] & (grid[x][y]["H2"] | grid[x][y]["H3"]))
        )


def can_move(grid):
    """
    Checks whether a car can move in any direction.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if y < GRID_SIZE - 1:
                can_move_down(x, y, grid)
            if y > 0:
                can_move_up(x, y, grid)
            if x < GRID_SIZE - 1:
                can_move_right(x, y, grid)
            if x > 0:
                can_move_left(x, y, grid)


def set_states(grid, board):
    """
    Sets the initial state of each cell.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            E.add_constraint(grid[x][y][board[y][x]])


def new_board(prev_board, direction, move_x, move_y):
    """
    Creates a new board after a move has been made.
    """

    filled_x = move_x
    filled_y = move_y

    next_board = prev_board
    if direction == "Right":
        if prev_board[move_y][move_x] == "H2":
            next_board[move_y][move_x - 1] = "E"
            next_board[move_y][move_x + 1] = "H2"

        elif prev_board[move_y][move_x] == "Red":
            next_board[move_y][move_x - 1] = "E"
            next_board[move_y][move_x + 1] = "Red"
        elif prev_board[move_y][move_x] == "H3":
            next_board[move_y][move_x - 2] = "E"
            next_board[move_y][move_x + 1] = "H3"

        filled_x = move_x + 1

    elif direction == "Left":
        if prev_board[move_y][move_x] == "H2":
            next_board[move_y][move_x + 1] = "E"
            next_board[move_y][move_x - 1] = "H2"
        elif prev_board[move_y][move_x] == "Red":
            next_board[move_y][move_x + 1] = "E"
            next_board[move_y][move_x - 1] = "Red"
        elif prev_board[move_y][move_x] == "H3":
            next_board[move_y][move_x + 2] = "E"
            next_board[move_y][move_x - 1] = "H3"

        filled_x = move_x - 1

    elif direction == "Up":
        if prev_board[move_y][move_x] == "V2":
            next_board[move_y + 1][move_x] = "E"
            next_board[move_y - 1][move_x] = "V2"
        elif prev_board[move_y][move_x] == "V3":
            next_board[move_y + 2][move_x] = "E"
            next_board[move_y - 1][move_x] = "V3"

        filled_y = move_y - 1

    elif direction == "Down":
        if prev_board[move_y][move_x] == "V2":
            next_board[move_y - 1][move_x] = "E"
            next_board[move_y + 1][move_x] = "V2"
        elif prev_board[move_y][move_x] == "V3":
            next_board[move_y - 2][move_x] = "E"
            next_board[move_y + 1][move_x] = "V3"

        filled_y = move_y + 1

    return next_board, filled_x, filled_y


def create_starting_board():
    """
    Selects a random starting board.
    """
    return random.choice(all_boards)


def format_board_for_print(board):
    """
    Formats the board for printing in the console.
    """
    formatted_board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[x][y] == "E":
                formatted_board[x][y] = "  "
            elif board[x][y] == "Red":
                formatted_board[x][y] = "R "
            else:
                formatted_board[x][y] = board[x][y]
    return formatted_board


def generate_256_colour_code(colour_number):
    """
    Generates a colour code for a given colour number.
    """
    return f"\033[48;5;{colour_number}m"


def extract_colour_number(colour_code):
    """
    Extracts the colour number from a colour code.
    """
    if f"\033[48;5;" in colour_code:
        colour_code = colour_code.replace("\033[48;5;", "")
        colour_code = colour_code.replace("m", "")
        return int(colour_code)


def colour_board_transfer(board):
    """
    Transfers the colours from the previous board to the new board.
    """
    new_row = None
    new_col = None
    transfer_colour = None

    colour_board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != "E" and prev_colour_board[row][col] != "":
                colour_board[row][col] = prev_colour_board[row][col]
            # If the cell was emptied
            elif board[row][col] == "E" and prev_colour_board[row][col] != "":
                transfer_colour = prev_colour_board[row][col]
            # If this cell was just filled
            elif board[row][col] != "E" and prev_colour_board[row][col] == "":
                new_row = row
                new_col = col

    colour_board[new_row][new_col] = transfer_colour

    return colour_board


def create_colour_board(board):
    """
    Creates a colour board for printing in the console.
    """

    # Initialize colour board with empty strings
    colour_board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    colours = [(generate_256_colour_code(num), name) for num, name in selected_colours]

    random.shuffle(colours)
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == "Red":
                colour_board[row][col] = "\033[48;5;9m"

            # Coloring horizontal cars 'H3'
            elif (
                board[row][col] == "H3"
                and col + 1 < len(board[row])
                and board[row][col + 1] == "H3"
                and col + 2 < len(board[row])
                and board[row][col + 2] == "H3"
                and colour_board[row][col] == ""
                and colour_board[row][col + 1] == ""
                and colour_board[row][col + 2] == ""
            ):
                colour_code, colour_name = colours.pop()
                colour_board[row][col] = colour_code
                colour_board[row][col + 1] = colour_code
                colour_board[row][col + 2] = colour_code

            # Coloring horizontal cars 'H2'
            elif (
                board[row][col] == "H2"
                and col + 1 < len(board[row])
                and board[row][col + 1] == "H2"
                and colour_board[row][col] == ""
                and colour_board[row][col + 1] == ""
            ):
                colour_code, colour_name = colours.pop()
                colour_board[row][col] = colour_code
                colour_board[row][col + 1] = colour_code

            # Improved logic for vertical cars 'V2' and 'V3'
            elif board[row][col] in ["V2", "V3"]:
                if (
                    row == 0 or board[row - 1][col] != board[row][col]
                ):  # Topmost part of the car
                    colour_code, colour_name = colours.pop()
                    car_length = 2 if board[row][col] == "V2" else 3
                    for offset in range(car_length):
                        if row + offset < len(board):
                            colour_board[row + offset][col] = colour_code

    return colour_board


def display_board(board, colour_board):
    """
    Displays the board in the console.
    """
    display_board = []
    for row in range(6):
        display_row = []
        for col in range(6):
            display_row.append(
                f"{colour_board[row][col]}{board[row][col]}{Style.RESET_ALL}"
            )
        display_board.append(display_row)
    return display_board


def print_table(final_board):
    """
    Prints the table in the console.
    """
    print("╒════╤════╤════╤════╤════╤════╕")
    for row in range(6):
        for col in range(5):
            print("│", final_board[row][col], "", end="")
        if row == 2:
            print("│", final_board[row][5], "")
        else:
            print("│", final_board[row][5], "│")
        if row == 5:
            print("╘════╧════╧════╧════╧════╧════╛")
        else:
            print("├────┼────┼────┼────┼────┼────┤")


def example_theory(E):
    """
    Builds an example full theory for the game.
    """
    set_states(
        current_grid, current_board
    )  # set the constraints of the state of each cell
    can_move(current_grid)
    only_one_state(current_grid)

    return E


def filter_true_results(result_dict):
    """
    Filters the results dictionary to only include the true results.
    """
    # Using dictionary comprehension to filter out True values
    true_values = {}
    for key in result_dict.keys():
        if result_dict[key]:
            true_values[key] = result_dict[key]
    # true_values = {key: value for key, value in result_dict.items() if value}
    return true_values


def filter_can_move(results):
    """
    Filters the results dictionary to only include the moves that can be made.
    """
    can_move_results_list = []
    for key in results.keys():
        if (
            "CMR" in repr(key)
            or "CML" in repr(key)
            or "CMD" in repr(key)
            or "CMU" in repr(key)
        ):
            move = key
            can_move_results_list.append(move)

    return can_move_results_list


def did_win(results):
    """
    Checks whether the game has been won.
    """
    # Assuming 'Red(5,2)' is the key format in the results dictionary
    for key in results:
        if str(key) == "Red(5,2)" and results[key]:
            return True
    return False


def translate_direction(move):
    """
    Translates the move into a direction.
    """
    direction = ""

    if repr(move)[:3] == "CMR":
        direction = "Right"
    elif repr(move)[:3] == "CML":
        direction = "Left"
    elif repr(move)[:3] == "CMD":
        direction = "Down"
    elif repr(move)[:3] == "CMU":
        direction = "Up"
    return direction


def extract_coordinates_from_move(move):
    """
    Extracts the coordinates from the move.
    """
    return move.x, move.y


def user_choose_move(move_list, colour_board):
    """
    Allows the user to choose a move.
    """
    option_num = 0
    for move in move_list:
        direction = translate_direction(move)
        move_x, move_y = extract_coordinates_from_move(move)

        if move_y == 2 and (direction == "Right" or direction == "Left"):
            colour_name = "Red"
        else:
            # Adjust coordinates for right and down moves
            move_x, move_y = find_leftmost_coordinate(current_board, move_x, move_y)
            move_x, move_y = find_topmost_coordinate(current_board, move_x, move_y)

            # Find the key in car_colour_mapping that ends with the coordinate string
            if colour_board[move_y][move_x] == "\033[48;5;9m":
                colour_name = "Red"
            elif colour_board[move_y][move_x] != "":
                colour_num = extract_colour_number(colour_board[move_y][move_x])
                colour_name = colour_mapping[colour_num]
            else:
                colour_name = "Unknown"

        print(f"Option: {option_num}: Move {colour_name} {direction}")
        option_num += 1

    chosen_option = None

    while True:
        try:
            chosen_option = int(
                input("Which move do you want to do? Input the number of the move: ")
            )

            if 0 <= chosen_option <= option_num - 1:
                break
            else:
                print(f"Please enter a choice between {0} and {option_num-1}.")

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    chosen_move = move_list[chosen_option]
    direction = translate_direction(chosen_move)
    move_x, move_y = extract_coordinates_from_move(chosen_move)

    return direction, move_x, move_y


def find_leftmost_coordinate(board, x, y):
    """
    Finds the leftmost coordinate of a car.
    """
    car_type = board[y][x]
    max_length = 2 if car_type == "H2" else 3 if car_type == "H3" else 1

    # Initialize variables to track the start of the car and its length
    start_x = x
    car_length = 0

    # Move leftwards to find the start of the car
    while start_x >= 0 and board[y][start_x] == car_type:
        start_x -= 1
        car_length += 1
        if car_length == max_length:
            break

    # Correct the start_x as it will be one step too far to the left
    start_x += 1

    return start_x, y


def find_topmost_coordinate(board, x, y):
    """
    Finds the topmost coordinate of a car.
    """
    car_type = board[y][x]  # Get the car type from the current position

    # Move upwards to find the start of the car
    while y > 0 and board[y - 1][x] == car_type:
        y -= 1

    return x, y


if __name__ == "__main__":
    clear_screen()
    current_board = create_starting_board()
    num_moves = 0

    while True:  # Until win state is reached
        E, Empty, H2, H3, V2, V3, CMR, CML, CMU, CMD, Red = initialize_encoding()

        if num_moves != 0:
            current_board, filled_x, filled_y = new_board(
                current_board, direction, move_x, move_y
            )

        current_grid = create_grid()
        current_grid = fill_grid(
            current_grid, Empty, H2, H3, V2, V3, CMR, CML, CMU, CMD, Red
        )

        T = example_theory(E)  # add constraints
        T = T.compile()  # compile model
        num_moves += 1
        # add 1 to the move counter

        # Display the board
        formatted_board = format_board_for_print(current_board)
        if num_moves == 1:
            colour_board = create_colour_board(current_board)
        else:
            colour_board = colour_board_transfer(current_board)

        final_board = display_board(formatted_board, colour_board)
        print_table(final_board)

        true_results = filter_true_results(
            T.solve()
        )  # filters so we only have the true results in the dictionary
        game_over = did_win(true_results)  # checks if red is in spot 5,2
        if game_over:
            print("You won! It took you", num_moves, "moves")
            exit()
        else:
            prev_colour_board = colour_board.copy()
            possible_moves = filter_can_move(
                true_results
            )  # filter so we only have the values with keys CMR, CML, CMD, CMU
            direction, move_x, move_y = user_choose_move(possible_moves, colour_board)
