
from colorama import Back, Style, Fore


# Original board
def create_board():
    board = [
            ['E', 'E', 'V2', 'H3', 'H3', 'H3'],
            ['V2', 'V2', 'V2', 'E', 'V2', 'V2'],
            ['V2', 'V2', 'Red', 'Red', 'V2', 'V2'],
            ['V2', 'H2', 'H2', 'H2', 'H2', 'V3'],
            ['V2', 'E', 'E', 'E', 'E', 'V3'],
            ['H2', 'H2', 'H3', 'H3', 'H3', 'V3']
        ]
    return board



def create_colour_board(board):
    # Initialize color board with empty strings
    color_board = [['' for _ in row] for row in board]

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

# Assign colors to H2, H3, V2, and V3 pairs
board = create_board()
color_board = create_colour_board(board)
final_board = display_board(board, color_board)


print("Display Board:")
print_table(final_board)
