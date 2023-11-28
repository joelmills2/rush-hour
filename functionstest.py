
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
previous_propositions = ['PE', 'PR', 'PH2', 'PH3', 'PV2', 'PV3']
next_propositions = ['NE', 'NR', 'NH2', 'NH3', 'NV2', 'NV3']

# Initialize an empty dictionary for the grid
prev_grid = {}
next_grid = {}

# Iterate through each row and column in the grid
for i in range(grid_size):
    for j in range(grid_size):
        
        # Initialize an empty dictionary for the propositions of the current cell
        cell_prev_propositions = {}
        
        # Iterate through each proposition identifier
        for prop in previous_propositions:
            
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
        for prop in next_propositions:
            
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

# Print the 'Previous' grid
#print_grid(prev_grid, 'Previous')

# Print the 'Next' grid
#print_grid(next_grid, 'Next')

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
 
    # Each cell can only one truth value on a given move
    for i in range (0,6):
        for j in range (0,6):
            constraint.add_exactly_one(
                E, 
                prev_grid[(i, j)]['PE'],
                prev_grid[(i, j)]['PR'],
                prev_grid[(i, j)]['PH2'],
                prev_grid[(i, j)]['PH3'],
                prev_grid[(i, j)]['PV2'],
                prev_grid[(i, j)]['PV3']
             )
            constraint.add_exactly_one(
                E, 
                next_grid[(i, j)]['NE'],
                next_grid[(i, j)]['NR'],
                next_grid[(i, j)]['NH2'],
                next_grid[(i, j)]['NH3'],
                next_grid[(i, j)]['NV2'],
                next_grid[(i, j)]['NV3']
             )

    # Each car has a fixed length of 2 or 3
    # Horizontal cars length 2

    # Horizontal cars length 3

    # Vertical cars length 2

    # Vertical cars length 3


    # Each car is continuous, ie. its cells are adjacent and in the same direction


    # The red car is a horizontal car of length 2


    # The red car is at row i=2


    # For a horizontal car, from previous (P) to next (N) state, the row (i) is the same 

    # Move the car:


    # H2 car & Empty to the right --> can move right & one before can move right


    # Checking where the head of cars that can move are
    for i in range(grid_size):
        for j in range (grid_size):
            
            if (i < 5):

                (prev_grid[(i, j)]['PH2'] & prev_grid[(i+1, j)]['PE']) >> prev_grid[(i, j)]['PCMR']

            if (i < 4):

                (prev_grid[(i, j)]['PH3'] & prev_grid[(i+1, j)]['PE']) >> prev_grid[(i, j)]['PCMR']
            
            if (i > 0):
                (prev_grid[(i, j)]['PH2'] & prev_grid[(i-1, j)]['PE']) >> prev_grid[(i, j)]['PCML']

            if (i > 1):
                (prev_grid[(i, j)]['PH3'] & prev_grid[(i-1, j)]['PE']) >> prev_grid[(i, j)]['PCML']


            if (j < 5):

                (prev_grid[(i, j)]['PV2'] & prev_grid[(i, j+1)]['PE']) >> prev_grid[(i, j)]['PCMD']

            if (j < 4):

                (prev_grid[(i, j)]['PV3'] & prev_grid[(i, j+1)]['PE']) >> prev_grid[(i, j)]['PCMD']
                                                                           
            if (j > 0):

                (prev_grid[(i, j)]['PV2'] & prev_grid[(i, j-1)]['PE']) >> prev_grid[(i, j)]['PCMU']

            if (j > 1): 

                (prev_grid[(i, j)]['PV3'] & prev_grid[(i, j-1)]['PE']) >> prev_grid[(i, j)]['PCMU']
    
    # Simulating Future Moves:

    no_change = False
    grid_list = [] # Stores all next_grid options to be outputed
    move_counter = 0 # How many moves can be made

    for i in range(grid_size): 
        for j in range (grid_size):


            no_change = False

            # The same spot cannnot have PCMR and PCML as these propositions are only true for the lead car.
            # The same spot cannnot have PCMR and PCMD as these propositions can only be treu for cells of different orientations.
            if (0 < i < grid_size):
                prev_grid[(i, j)]['CMR'] & prev_grid[(i, j)]['H2'] >> next_grid[(i+1, j)]['H2'] & next_grid[(i, j)]['H2'] & next_grid[(i-1, j)]['E']
                prev_grid[(i, j)]['CML'] & prev_grid[(i, j)]['H2'] >> next_grid[(i-1, j)]['H2'] & next_grid[(i, j)]['H2'] & next_grid[(i+1, j)]['E']

            if (1 < i < grid_size-1):
                prev_grid[(i, j)]['CMR'] & prev_grid[(i, j)]['H3'] >> next_grid[(i+1, j)]['H3'] & next_grid[(i, j)]['H3'] & next_grid[(i-1, j)]['H3'] & next_grid[(i-2, j)]['E']
                prev_grid[(i, j)]['CML'] & prev_grid[(i, j)]['H3'] >> next_grid[(i-1, j)]['H3'] & next_grid[(i, j)]['H3'] & next_grid[(i+1, j)]['H3'] & next_grid[(i+2, j)]['E']              

            if (0 < j < grid_size):
                prev_grid[(i, j)]['CMD'] & prev_grid[(i, j)]['V2'] >> next_grid[(i, j+1)]['V2'] & next_grid[(i, j)]['V2'] & next_grid[(i, j-1)]['E']
                prev_grid[(i, j)]['CMU'] & prev_grid[(i, j)]['V2'] >> next_grid[(i, j-1)]['V2'] & next_grid[(i, j)]['V2'] & next_grid[(i, j+1)]['E']

            if (1 < j < grid_size-1):
                prev_grid[(i, j)]['CMD'] & prev_grid[(i, j)]['V3'] >> next_grid[(i, j+1)]['V3'] & next_grid[(i, j)]['V3'] & next_grid[(i, j-1)]['V3'] & next_grid[(i, j-2)]['E']
                prev_grid[(i, j)]['CMU'] & prev_grid[(i, j)]['V3'] >> next_grid[(i, j-1)]['V3'] & next_grid[(i, j)]['V3'] & next_grid[(i, j+1)]['V3'] & next_grid[(i, j+2)]['E']

            ~(prev_grid[(i,j)]['CMR']|prev_grid[(i,j)]['CML']|prev_grid[(i,j)]['CMD']|prev_grid[(i,j)]['CMU']) >> no_change

            if ~no_change:
                grid_list.append(next_grid)
                move_counter+=1


    # Outputting Board Function
    # Currently only works if we get rid of P and N (they are no longer needed)
    def print_board(grid):  
        for i in range(grid_size):
            row = ""
            for j in range (grid_size):
                if grid[(i,j)]['E']:
                    row 
                    






            # Next grid is the same but with the move
            # Print Next grid 
            # Make Prev Grid = Next Grid
            # Prompt for next move
            prev_grid[(i, j)]['PCMR'] & prev_grid[(i, j)]['H2'] >> next_grid[(i+1, j)]['H2'] & next_grid[(i, j)]['NE']
            # Repete for all, find a way to know once a move has been made and save that as a grid in a grid of after grids
            # Output 


            


    for i in range(grid_size-1):
        for j in range(grid_size):
            #CM is can move proposition
            (prev_grid[(i, j)]['PH2'] & prev_grid[(i+1, j)]['PE']) >> (prev_grid[(i, j)]['PCM'] & prev_grid[(i-1, j)]['PCM'])

    # H3 car & Empty to the right --> can move right & one before can move right & one before can move right
    for i in range(grid_size-2):
        for j in range(grid_size):
            #CM is can move proposition
            (prev_grid[(i, j)]['PH3'] & prev_grid[(i+1, j)]['PE']) >> (prev_grid[(i, j)]['PCM'] & prev_grid[(i-1, j)]['PCM'] & prev_grid[(i-2, j)]['PCM'])

    # V2 car & Empty below --> can move down & one above can move down
    for i in range(grid_size):
        for j in range(grid_size-1):
            #CM is can move proposition
            (prev_grid[(i, j)]['PV2'] & prev_grid[(i, j+1)]['PE']) >> (prev_grid[(i, j)]['PCM'] & prev_grid[(i, j-1)]['PCM'])

    # V3 car & Empty below --> can move down & one before can move down & one before can move down
    for i in range(grid_size):
        for j in range(grid_size-2):
            #CM is can move proposition
            (prev_grid[(i, j)]['PV3'] & prev_grid[(i, j+1)]['PE']) >> (prev_grid[(i, j)]['PCM'] & prev_grid[(i, j-1)]['PCM'] & prev_grid[(i, j-2)]['PCM'])


    # H2 car & Empty to the right --> can move right & one before can move right
    for i in range(grid_size,1,-1):
        for j in range(grid_size,0,-1):
            #CM is can move proposition
            (prev_grid[(i, j)]['PH2'] & prev_grid[(i-1, j)]['PE']) >> (prev_grid[(i, j)]['PCM'] & prev_grid[(i+1, j)]['PCM'])



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
