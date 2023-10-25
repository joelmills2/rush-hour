
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
            proposition_object = RushHourPropositions(f"{i}{j}{prop}")
            
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
            proposition_object = RushHourPropositions(f"{i}{j}{prop}")
            
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
print_grid(prev_grid, 'Previous')

# Print the 'Next' grid
print_grid(next_grid, 'Next')

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    # Add custom constraints by creating formulas with the variables you created. 
    E.add_constraint((a | b) & ~x)
    # Implication
    E.add_constraint(y >> z)
    # Negate a formula
    E.add_constraint(~(x & y))
    # You can also add more customized "fancy" constraints. Use case: you don't want to enforce "exactly one"
    # for every instance of BasicPropositions, but you want to enforce it for a, b, and c.:
    constraint.add_exactly_one(E, a, b, c)

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
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
