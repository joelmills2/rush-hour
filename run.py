
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"

# Encoding that will store all of your constraints
E = Encoding()

# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class RushHourPropositions:

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"A.{self.data}"


grid_size = 6
propositions = ['E', 'RED', 'H2', 'H3', 'V2', 'V3', 'CMR', 'CML', 'CMD', 'CMU']

# Initialize an empty dictionary for the grid
prev_grid = {}
next_grid = {}

# Iterate through each row and column in the grid
for i in range(grid_size):
    for j in range(grid_size):
        
        # Initialize an empty dictionary for the propositions of the current cell
        cell_prev_propositions = {}
        
        # Iterate through each proposition identifier
        for prop in propositions:
            
            # Create a new instance of RushHourPropositions for the current proposition
            # The identifier is created by concatenating the coordinates and proposition identifier
            proposition_object = RushHourPropositions(f"{prop}{i}{j}")
            
            # Add the new RushHourPropositions instance to the cell_propositions dictionary
            cell_prev_propositions[prop] = proposition_object
        
        # Once all propositions for the current cell have been created,
        # add the cell_propositions dictionary to the grid dictionary
        prev_grid[(i, j)] = cell_prev_propositions

# Iterate through each row and column in the grid
for i in range(grid_size):
    for j in range(grid_size):
        
        # Initialize an empty dictionary for the propositions of the current cell
        cell_next_propositions = {}
        
        # Iterate through each proposition identifier
        for prop in propositions:
            
            # Create a new instance of RushHourPropositions for the current proposition
            # The identifier is created by concatenating the coordinates and proposition identifier
            proposition_object = RushHourPropositions(f"{prop}{i}{j}")
            
            # Add the new RushHourPropositions instance to the cell_propositions dictionary
            cell_next_propositions[prop] = proposition_object
        
        # Once all propositions for the current cell have been created,
        # add the cell_propositions dictionary to the grid dictionary
        next_grid[(i, j)] = cell_next_propositions

# Function to print a grid
def print_grid(grid, grid_name):
    print(f"Grid: {grid_name}")
    # Iterate through each cell in the grid
    for coords, cell_propositions in grid.items():
        # Iterate through each proposition in the current cell
        for prop_id, prop_object in cell_propositions.items():
            # Print the coordinates, proposition identifier, and proposition object identifier
            print(f"Coordinates: {coords}, Proposition Identifier: {prop_id}")
    print("\n")  # Print a newline between grids for readability


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
 
    # Each cell can only one truth value on a given move, and a cell with no cars cannot move
    for i in range (0,6):
        for j in range (0,6):
            constraint.add_exactly_one(
                E, 
                prev_grid[(i, j)]['E'],
                prev_grid[(i, j)]['RED'],
                prev_grid[(i, j)]['H2'],
                prev_grid[(i, j)]['H3'],
                prev_grid[(i, j)]['V2'],
                prev_grid[(i, j)]['V3']
             )
            constraint.add_exactly_one(
                E, 
                next_grid[(i, j)]['E'],
                next_grid[(i, j)]['RED'],
                next_grid[(i, j)]['H2'],
                next_grid[(i, j)]['H3'],
                next_grid[(i, j)]['V2'],
                next_grid[(i, j)]['V3']
             )
            constraint.add_exactly_one(
                E,
                prev_grid[(i, j)]['E'],
                prev_grid[(i, j)]['CMR'],
                prev_grid[(i, j)]['CML'],
                prev_grid[(i, j)]['CMD'],
                prev_grid[(i, j)]['CMU']
            )
            constraint.add_exactly_one(
                E,
                next_grid[(i, j)]['E'],
                next_grid[(i, j)]['CMR'],
                next_grid[(i, j)]['CML'],
                next_grid[(i, j)]['CMD'],
                next_grid[(i, j)]['CMU']
            )


    # Each car has a fixed length of 2 or 3 - if a cell has a car, one or more adjacent cells must have the same car (all cars have a height of 1)
    # Horizontal cars length 2
    for row in range(grid_size):
        for col in range(grid_size - 1):  # Subtract 1 to avoid index out of range
            E.add_constraint(
                prev_grid[(row, col)]['H2'] >> prev_grid[(row, col + 1)]['H2']
            )

    for row in range(grid_size):
        for col in range(grid_size - 1):  # Subtract 1 to avoid index out of range
            E.add_constraint(
                next_grid[(row, col)]['H2'] >> next_grid[(row, col + 1)]['H2']
            )

    # Horizontal cars length 3
    for row in range(grid_size):
        for col in range(grid_size - 2):
            E.add_constraint(
                prev_grid[(row, col)]['H3'] >> (prev_grid[(row, col + 1)]['H3'] & prev_grid[(row, col + 2)]['H3'])
            )
    
    for row in range(grid_size):
        for col in range(grid_size - 2):
            E.add_constraint(
                next_grid[(row, col)]['H3'] >> (next_grid[(row, col + 1)]['H3'] & next_grid[(row, col + 2)]['H3'])
            )
            

    # Vertical cars length 2
    for col in range(grid_size):
        for row in range(grid_size - 1):
            E.add_constraint(
                prev_grid[(row, col)]['V2'] >> prev_grid[(row + 1, col)]['V2']
            )
    
    for col in range(grid_size):
        for row in range(grid_size - 1):
            E.add_constraint(
                next_grid[(row, col)]['V2'] >> next_grid[(row + 1, col)]['V2']
            )

    # Vertical cars length 3
    for col in range(grid_size):
        for row in range(grid_size - 2):
            E.add_constraint(
                prev_grid[(row, col)]['V3'] >> (prev_grid[(row + 1, col)]['V3'] & prev_grid[(row + 2, col)]['V3'])
            )
    
    for col in range(grid_size):
        for row in range(grid_size - 2):
            E.add_constraint(
                next_grid[(row, col)]['V3'] >> (next_grid[(row + 1, col)]['V3'] & next_grid[(row + 2, col)]['V3'])
            )


    # The red car is a horizontal car of length 2, and must be in the 3rd row (i = 2)

    # For a horizontal car, from previous (P) to next (N) state, the row (i) is the same (ie. a constant k), but the column j can change

    # For a vertical car, from previous (P) to next (N) state, the column (j) is the same (ie. a constant k), but the row i can change

    # Cars have a fixed size

    # No vehicles moving horizontally can be in the same row as the red car, ie. i != 2


    # We start with some initial configuration, where every cell must be assigned a value


    # The game is complete when no cars are blocking the red car from exiting the board, ie. R_{2j} > P_{2j} for all j in [0,5]


    # When one part of a car moves, the rest of the car must move with it, ie. H3_{10} && H3_{11} && H3_{12} -> H3_{12} && H3_{13} && H3_{14}

    
    # Checking if a car has any valid moves
    for i in range(grid_size):
        for j in range (grid_size):
            if (i < 5):
                (prev_grid[(i, j)]['H2'] & prev_grid[(i+1, j)]['E']) >> prev_grid[(i, j)]['CMR']

            if (i < 4):
                (prev_grid[(i, j)]['H3'] & prev_grid[(i+1, j)]['E']) >> prev_grid[(i, j)]['CMR']
            if (i > 0):
                (prev_grid[(i, j)]['H2'] & prev_grid[(i-1, j)]['E']) >> prev_grid[(i, j)]['CML']

            if (i > 1):
                (prev_grid[(i, j)]['H3'] & prev_grid[(i-1, j)]['E']) >> prev_grid[(i, j)]['CML']


            if (j < 5):

                (prev_grid[(i, j)]['V2'] & prev_grid[(i, j+1)]['E']) >> prev_grid[(i, j)]['CMD']

            if (j < 4):

                (prev_grid[(i, j)]['V3'] & prev_grid[(i, j+1)]['E']) >> prev_grid[(i, j)]['CMD']
                                                                           
            if (j > 0):

                (prev_grid[(i, j)]['V2'] & prev_grid[(i, j-1)]['E']) >> prev_grid[(i, j)]['CMU']

            if (j > 1): 

                (prev_grid[(i, j)]['V3'] & prev_grid[(i, j-1)]['E']) >> prev_grid[(i, j)]['CMU']
    


    # Simulating the movement of a car; updating the grid

    no_change = False
    grid_list = [] # Stores all next_grid options to be outputed
    move_counter = 0 # How many moves can be made
            
    for i in range(grid_size): 
        for j in range (grid_size):

            no_change = False
            print ('i', i, 'j', j)
            print (prev_grid[(i, j)]['E'])
            # The same spot cannnot have PCMR and PCML as these propositions are only true for the lead car.
            # The same spot cannnot have PCMR and PCMD as these propositions can only be treu for cells of different orientations.
            if (0 < i < grid_size - 1):
                prev_grid[(i, j)]['CMR'] & prev_grid[(i, j)]['H2'] >> next_grid[(i+1, j)]['H2'] & next_grid[(i, j)]['H2'] & next_grid[(i-1, j)]['E']
                prev_grid[(i, j)]['CML'] & prev_grid[(i, j)]['H2'] >> next_grid[(i-1, j)]['H2'] & next_grid[(i, j)]['H2'] & next_grid[(i+1, j)]['E']

            if (1 < i < grid_size - 2):
                prev_grid[(i, j)]['CMR'] & prev_grid[(i, j)]['H3'] >> next_grid[(i+1, j)]['H3'] & next_grid[(i, j)]['H3'] & next_grid[(i-1, j)]['H3'] & next_grid[(i-2, j)]['E']
                prev_grid[(i, j)]['CML'] & prev_grid[(i, j)]['H3'] >> next_grid[(i-1, j)]['H3'] & next_grid[(i, j)]['H3'] & next_grid[(i+1, j)]['H3'] & next_grid[(i+2, j)]['E']              

            if (0 < j < grid_size - 1):
                prev_grid[(i, j)]['CMD'] & prev_grid[(i, j)]['V2'] >> next_grid[(i, j+1)]['V2'] & next_grid[(i, j)]['V2'] & next_grid[(i, j-1)]['E']
                prev_grid[(i, j)]['CMU'] & prev_grid[(i, j)]['V2'] >> next_grid[(i, j-1)]['V2'] & next_grid[(i, j)]['V2'] & next_grid[(i, j+1)]['E']

            if (1 < j < grid_size - 2):
                prev_grid[(i, j)]['CMD'] & prev_grid[(i, j)]['V3'] >> next_grid[(i, j+1)]['V3'] & next_grid[(i, j)]['V3'] & next_grid[(i, j-1)]['V3'] & next_grid[(i, j-2)]['E']
                prev_grid[(i, j)]['CMU'] & prev_grid[(i, j)]['V3'] >> next_grid[(i, j-1)]['V3'] & next_grid[(i, j)]['V3'] & next_grid[(i, j+1)]['V3'] & next_grid[(i, j+2)]['E']

            if (prev_grid[(i,j)]['CMR']|prev_grid[(i,j)]['CML']|prev_grid[(i,j)]['CMD']|prev_grid[(i,j)]['CMU']):
                no_change == True

            if ~no_change:
                grid_list.append(next_grid)
                move_counter+=1

    return E

if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for i in range(grid_size):
        for j in range(grid_size):
            for prop in previous_propositions:
                prop_var = prev_grid[(i, j)][prop]
                likelihood_value = likelihood(T, prop_var)
                print(f" {prop_var}: {likelihood_value:.2f}")
    print()
