
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

from colorama import Back, Style, Fore

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# Grid dimensions
GRID_SIZE = 6

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

# Innitialize Empty Grid
def create_grid():
    new_grid = [[{} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return new_grid

# Fill Grid with propositions
def fill_grid(grid):
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
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):

            if y == 2:
                constraint.add_exactly_one(E, [
                    grid[x][y]["E"],
                    grid[x][y]["H2"],
                    grid[x][y]["H3"],
                    grid[x][y]["V2"],
                    grid[x][y]["V3"],
                    grid[x][y]["Red"]
                ])

            else:
                constraint.add_exactly_one(E, [
                    grid[x][y]["E"],
                    grid[x][y]["H2"],
                    grid[x][y]["H3"],
                    grid[x][y]["V2"],
                    grid[x][y]["V3"]
                ])

def can_move_down(x,y,grid):
    E.add_constraint((grid[x][y]['V2'] & grid[x][y+1]['E']) >> grid[x][y]['CMD'])
    E.add_constraint((grid[x][y]['V3'] & grid[x][y+1]['E']) >> grid[x][y]['CMD'])
    E.add_constraint(grid[x][y]['CMD'] >> (grid[x][y+1]['E'] & (grid[x][y]['V2'] | grid[x][y]['V3'])))

def can_move_up(x,y,grid):
    E.add_constraint((grid[x][y]['V2'] & grid[x][y-1]['E']) >> grid[x][y]['CMU'])
    E.add_constraint((grid[x][y]['V3'] & grid[x][y-1]['E']) >> grid[x][y]['CMU'])
    E.add_constraint(grid[x][y]['CMU'] >> (grid[x][y-1]['E'] & (grid[x][y]['V2'] | grid[x][y]['V3'])))


def can_move_right(x,y,grid):
    E.add_constraint((grid[x][y]['H2'] & grid[x+1][y]['E']) >> grid[x][y]['CMR'])
    E.add_constraint((grid[x][y]['H3'] & grid[x+1][y]['E']) >> grid[x][y]['CMR'])
    if y == 2:
        E.add_constraint((grid[x][y]['Red'] & grid[x+1][y]['E']) >> grid[x][y]['CMR'])
        E.add_constraint(grid[x][y]['CMR'] >> (grid[x+1][y]['E'] & (grid[x][y]['H2'] | grid[x][y]['H3'] | grid[x][y]['Red'])))
    else:
        E.add_constraint(grid[x][y]['CMR'] >> (grid[x+1][y]['E'] & (grid[x][y]['H2'] | grid[x][y]['H3'])))



def can_move_left(x,y,grid):
    E.add_constraint((grid[x][y]['H2'] & grid[x-1][y]['E']) >> grid[x][y]['CML'])
    E.add_constraint((grid[x][y]['H3'] & grid[x-1][y]['E']) >> grid[x][y]['CML'])
    if y == 2:
        E.add_constraint((grid[x][y]['Red'] & grid[x-1][y]['E']) >> grid[x][y]['CML'])
        E.add_constraint(grid[x][y]['CML'] >> (grid[x-1][y]['E'] & (grid[x][y]['H2'] | grid[x][y]['H3'] | grid[x][y]['Red'])))
    else:
        E.add_constraint(grid[x][y]['CML'] >> (grid[x-1][y]['E'] & (grid[x][y]['H2'] | grid[x][y]['H3'])))


def can_move(grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (y < GRID_SIZE-1):
                can_move_down(x,y,grid)
            if (y > 0):
                can_move_up(x,y,grid)
            if (x < GRID_SIZE-1):
                can_move_right(x,y,grid)
            if (x > 0):
                can_move_left(x,y,grid)


# Building Initial Board:
def set_states(grid,board):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            E.add_constraint(grid[x][y][board[y][x]])

def new_board(prev_board, direction, move_x, move_y):
    next_board = prev_board
    if direction == "Right":
            if prev_board[move_y][move_x] == 'H2':
                next_board[move_y][move_x-1] = 'E'
                next_board[move_y][move_x+1] = 'H2'
            elif prev_board[move_y][move_x] == 'Red':
                next_board[move_y][move_x-1] = 'E'
                next_board[move_y][move_x+1] = 'Red'
            elif prev_board[move_y][move_x] == 'H3':
                next_board[move_y][move_x-2] = 'E'
                next_board[move_y][move_x+1] = 'H2'
    elif direction == "Left":
            if prev_board[move_y][move_x] == 'H2':
                next_board[move_y][move_x+1] = 'E'
                next_board[move_y][move_x-1] = 'H2'
            elif prev_board[move_y][move_x] == 'Red':
                next_board[move_y][move_x+1] = 'E'
                next_board[move_y][move_x-1] = 'Red'
            elif prev_board[move_y][move_x] == 'H3':
                next_board[move_y][move_x+2] = 'E'
                next_board[move_y][move_x-1] = 'H2'
    elif direction == "Up":
            if prev_board[move_y][move_x] == 'V2':
                next_board[move_y+1][move_x] = 'E'
                next_board[move_y-1][move_x] = 'V2'
            elif prev_board[move_y][move_x] == 'V3':
                next_board[move_y+2][move_x] = 'E'
                next_board[move_y-1][move_x] = 'V2'
    elif direction == "Down":
            if prev_board[move_y][move_x] == 'V2':
                next_board[move_y-1][move_x] = 'E'
                next_board[move_y+1][move_x] = 'V2'
            elif prev_board[move_y][move_x] == 'V3':
                next_board[move_y-2][move_x] = 'E'
                next_board[move_y+1][move_x] = 'V2'
            
    return next_board

def create_starting_board():
    board = [
            ['E', 'E', 'V2', 'H3', 'H3', 'H3'],
            ['V2', 'V2', 'V2', 'E', 'V2', 'V2'],
            ['V2', 'V2', 'Red', 'Red', 'V2', 'V2'],
            ['V2', 'H2', 'H2', 'H2', 'H2', 'V3'],
            ['V2', 'E', 'E', 'E', 'E', 'V3'],
            ['H2', 'H2', 'H3', 'H3', 'H3', 'V3']
        ]
    return board



def format_board_for_print(board):
    formatted_board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if board[x][y] == 'E':
                formatted_board[x][y] = '  '
            elif board[x][y] == 'Red':
                formatted_board[x][y] = 'R '
            else:
                formatted_board[x][y] = board[x][y]
    return formatted_board

def create_colour_board(board):
    # Initialize color board with empty strings
    color_board =  [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]   

    # Helper function to assign colors to H2, H3, V2, and V3 pairs
    colours = [getattr(Back, color) for color in dir(Back) if color.isupper()]
    colours.remove(Back.RED)
    colours.remove(Back.LIGHTRED_EX)
    colours.extend(colours)
    colours.extend(colours)

    print(Style.RESET_ALL)
    for row in range(len(board)):  # Iterate up to the last row
        for col in range(len(board[row])):
            if board[row][col] == 'R ':
                color_board[row][col] = Back.RED
            if board[row][col] == 'H3' and col + 1 < len(board[row]) and board[row][col + 1] == 'H3' and col + 2 < len(board[row]) and board[row][col + 2] == 'H3':
                color = colours.pop()
                color_board[row][col] = color
                color_board[row][col + 1] = color
                color_board[row][col + 2] = color
                col += 2
            elif board[row][col] == 'H2' and col + 1 < len(board[row]) and board[row][col + 1] == 'H2' and color_board[row][col] == '':
                color = colours.pop()
                color_board[row][col] = color
                color_board[row][col + 1] = color
                col += 1
            elif board[row][col] == 'V2' and row + 1 < len(board) and board[row + 1][col] == 'V2' and color_board[row][col] == '' and color_board[row + 1][col] == '':
                color = colours.pop()
                color_board[row][col] = color
                color_board[row + 1][col] = color
            elif board[row][col] == 'V3' and row + 1 < len(board) and board[row + 1][col] == 'V3' and row + 2 < len(board) and board[row + 2][col] == 'V3' and color_board[row][col] == '' and color_board[row + 1][col] == '' and color_board[row + 2][col] == '':
                color = colours.pop()
                color_board[row][col] = color
                color_board[row + 1][col] = color
                color_board[row + 2][col] = color
    return color_board

def display_board(board, color_board):
    display_board = []
    for row in range(6):
        display_row = []
        for col in range(6):
            display_row.append(f'{color_board[row][col]}{board[row][col]}{Style.RESET_ALL}')
        display_board.append(display_row)
    return display_board

def print_table(final_board):
    print("╒════╤════╤════╤════╤════╤════╕")
    for row in range(6):
        for col in range(5):
            print("│",final_board[row][col], "", end="")
        if row == 2:
            print("│",final_board[row][5], "")
        else:
            print("│",final_board[row][5], "│")
        if row == 5:
            print("╘════╧════╧════╧════╧════╧════╛")
        else:
            print("├────┼────┼────┼────┼────┼────┤")





# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

num_moves = 0

def example_theory():
    set_states(current_grid, current_board) # set the constraints of the state of each cell
    can_move(current_grid)
    only_one_state(current_grid)


    return E

def filter_true_results(result_dict):
    # Using dictionary comprehension to filter out True values
    true_values = {key: value for key, value in result_dict.items() if value}
    return true_values

def filter_can_move(results):
    can_move_results_list = []
    for key in results.keys():
        if ("CMR" in repr(key) or "CML" in repr(key) or "CMD" in repr(key) or "CMU" in repr(key)):
            move = key
            can_move_results_list.append(move)

    return can_move_results_list


def did_win(results):
    return "Red(5,2)" in results

def translate_direction(move):

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


def user_choose_move(move_list):
    option_num = 0
    for move in move_list:
        direction = translate_direction(move)
        print("Option:",option_num, repr(move)[3:], direction)
        option_num+=1

    option_num = (int)(input("Which move do you want to do? Input the number of the move: "))

    direction = translate_direction(move_list[option_num])
    move_x = repr(move_list[option_num])[4:5]
    move_y = repr(move_list[option_num])[6:7]

    return direction, (int)(move_x), (int)(move_y)


if __name__ == "__main__":

    current_board = create_starting_board()

    while True: # Until win state is reached
        if num_moves != 0:
            current_board = new_board(current_board, direction, move_x, move_y)

        current_grid = create_grid()
        current_grid = fill_grid(current_grid)
        

        T = example_theory() # add constraints
        T = T.compile() # compile model
        print("\nSatisfiable: %s" % T.satisfiable()) # will be removed in final product
        print("# Solutions: %d" % count_solutions(T)) # will be removed in final product
        num_moves += 1; # add 1 to the move counter
        print(T.solve())
    
        # Display the board
        formatted_board = format_board_for_print(current_board)
        color_board = create_colour_board(formatted_board)
        final_board = display_board(formatted_board, color_board)
        print("Display Board:")
        print_table(final_board)
    
        true_results = filter_true_results(T.solve()) # filters so we only have the true results in the dictionary
        game_over = did_win(true_results) # checks if red is in spot 5,2
        if game_over:
            #display_game_over(num_moves)
            break
        else:
            possible_moves = filter_can_move(true_results) # filter so we only have the values with keys CMR, CML, CMD, CMU
            direction, move_x, move_y = user_choose_move(possible_moves)