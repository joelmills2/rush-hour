
from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood

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
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"Empty({self.i},{self.j})"

@proposition(E)
class Red:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"Red({self.i},{self.j})"

@proposition(E)
class H2:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"H2({self.i},{self.j})"
   
@proposition(E)
class H3:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"H3({self.i},{self.j})"
   
@proposition(E)
class V2:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"V2({self.i},{self.j})"
   
@proposition(E)
class V3:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"V3({self.i},{self.j})"
   
@proposition(E)
class CMR:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"CMR({self.i},{self.j})"

@proposition(E)
class CML:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"CML({self.i},{self.j})"
        
   
@proposition(E)
class CMU:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"CMU({self.i},{self.j})"
   
@proposition(E)
class CMD:
    def __init__(self, i, j):
        self.i, self.j = i, j

    def __repr__(self):
        return f"CMD({self.i},{self.j})"

# Innitialize Empty Grid
def create_grid():
    new_grid = [[{} for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    return new_grid

# Fill Grid with propositions
def fill_grid(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            grid[i][j]["E"] = Empty(i, j)
            grid[i][j]["H2"] = H2(i, j)
            grid[i][j]["H3"] = H3(i, j)
            grid[i][j]["V2"] = V2(i, j)
            grid[i][j]["V3"] = V3(i, j)
            grid[i][j]["CMR"] = CMR(i, j)
            grid[i][j]["CML"] = CML(i, j)
            grid[i][j]["CMU"] = CMU(i, j)
            grid[i][j]["CMD"] = CMD(i, j)
            if i == 2:
                grid[i][j]["Red"] = Red(i, j)
    return grid


# CONSTRAINT FUNCTIONS
def only_one_state(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            if i == 2:
                constraint.add_exactly_one(E, [
                    grid[i][j]["E"],
                    grid[i][j]["H2"],
                    grid[i][j]["H3"],
                    grid[i][j]["V2"],
                    grid[i][j]["V3"],
                    grid[i][j]["Red"]
                ])

            else:
                constraint.add_exactly_one(E, [
                    grid[i][j]["E"],
                    grid[i][j]["H2"],
                    grid[i][j]["H3"],
                    grid[i][j]["V2"],
                    grid[i][j]["V3"]
                ])

def can_move(grid):
    for i in range(GRID_SIZE):
        for j in range (GRID_SIZE):

            if (i < GRID_SIZE-1):
                E.add_constraint((~grid[i][j]['H2'] | ~grid[i+1][j]['E'] | grid[i][j]['CMR']) & (grid[i][j]['H2'] | ~grid[i][j]['CMR']) & (grid[i+1][j]['E'] | ~grid[i][j]['CMR']))

            if (i < GRID_SIZE-2):
                E.add_constraint((~grid[i][j]['H3'] | ~grid[i+1][j]['E'] | grid[i][j]['CMR']) & (grid[i][j]['H3'] | ~grid[i][j]['CMR']) & (grid[i+1][j]['E'] | ~grid[i][j]['CMR']))
           
            if (i > 0):
                E.add_constraint((~grid[i][j]['H2'] | ~grid[i-1][j]['E'] | grid[i][j]['CML']) & (grid[i][j]['H2'] | ~grid[i][j]['CML']) & (grid[i-1][j]['E'] | ~grid[i][j]['CML']))
            
            if (i > 1):
                E.add_constraint((~grid[i][j]['H3'] | ~grid[i-1][j]['E'] | grid[i][j]['CML']) & (grid[i][j]['H3'] | ~grid[i][j]['CML']) & (grid[i-1][j]['E'] | ~grid[i][j]['CML']))

            if (j < GRID_SIZE-1):
                E.add_constraint((~grid[i][j]['V2'] | ~grid[i][j+1]['E'] | grid[i][j]['CMD']) & (grid[i][j]['V2'] | ~grid[i][j]['CMD']) & (grid[i][j+1]['E'] | ~grid[i][j]['CMD']))

            if (j < GRID_SIZE-2):
                E.add_constraint((~grid[i][j]['V3'] | ~grid[i][j+1]['E'] | grid[i][j]['CMD']) & (grid[i][j]['V3'] | ~grid[i][j]['CMD']) & (grid[i][j+1]['E'] | ~grid[i][j]['CMD']))
                             
            if (j > 0):
                E.add_constraint((~grid[i][j]['V2'] | ~grid[i][j-1]['E'] | grid[i][j]['CMU']) & (grid[i][j]['V2'] | ~grid[i][j]['CMU']) & (grid[i][j-1]['E'] | ~grid[i][j]['CMU']))

            if (j > 1):
                E.add_constraint((~grid[i][j]['V3'] | ~grid[i][j-1]['E'] | grid[i][j]['CMU']) & (grid[i][j]['V3'] | ~grid[i][j]['CMU']) & (grid[i][j-1]['E'] | ~grid[i][j]['CMU']))

            if (i==2):
                E.add_constraint((~grid[i][j]['Red'] | ~grid[i+1][j]['E'] | grid[i][j]['CMR']) & (grid[i][j]['Red'] | ~grid[i][j]['CMR']) & (grid[i+1][j]['E'] | ~grid[i][j]['CMR']))
                E.add_constraint((~grid[i][j]['Red'] | ~grid[i-1][j]['E'] | grid[i][j]['CML']) & (grid[i][j]['Red'] | ~grid[i][j]['CML']) & (grid[i-1][j]['E'] | ~grid[i][j]['CML']))


# Building Initial Board:
def starting_board(grid):
    E.add_constraint(grid[0][0]['E'])
    E.add_constraint(grid[0][1]['E'])
    E.add_constraint(grid[0][2]['E'])
    E.add_constraint(grid[0][3]['E'])
    E.add_constraint(grid[0][4]['E'])
    E.add_constraint(grid[0][5]['E'])
    E.add_constraint(grid[1][0]['E'])
    E.add_constraint(grid[1][1]['E'])
    E.add_constraint(grid[1][2]['E'])
    E.add_constraint(grid[1][3]['E'])
    E.add_constraint(grid[1][4]['E'])
    E.add_constraint(grid[1][5]['E'])
    E.add_constraint(grid[2][0]['E'])
    E.add_constraint(grid[2][1]['E'])
    E.add_constraint(grid[2][2]['E'])
    E.add_constraint(grid[2][3]['E'])
    E.add_constraint(grid[2][4]['E'])
    E.add_constraint(grid[2][5]['E'])
    E.add_constraint(grid[3][0]['E'])
    E.add_constraint(grid[3][1]['E'])
    E.add_constraint(grid[3][2]['H2'])
    E.add_constraint(grid[3][3]['H2'])
    E.add_constraint(grid[3][4]['E'])
    E.add_constraint(grid[3][5]['E'])
    E.add_constraint(grid[4][0]['E'])
    E.add_constraint(grid[4][1]['E'])
    E.add_constraint(grid[4][2]['E'])
    E.add_constraint(grid[4][3]['E'])
    E.add_constraint(grid[4][4]['E'])
    E.add_constraint(grid[4][5]['E'])
    E.add_constraint(grid[5][0]['E'])
    E.add_constraint(grid[5][1]['E'])
    E.add_constraint(grid[5][2]['E'])
    E.add_constraint(grid[5][3]['E'])
    E.add_constraint(grid[5][4]['E'])
    E.add_constraint(grid[5][5]['E'])


#Create Previous Grid
prev_grid = create_grid()
prev_grid = fill_grid(prev_grid)



# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    can_move(prev_grid)
    only_one_state(prev_grid)
    # If we choose to loop through the game this would be if on first itteration
    starting_board(prev_grid)
    return E


if __name__ == "__main__":

    T = example_theory()
    # Don't compile until you're finished adding all your constraints!
    T = T.compile()
    print(E.introspect())
    # After compilation (and only after), you can check some of the properties
    # of your model:
    print("\nSatisfiable: %s" % T.satisfiable())
    print("# Solutions: %d" % count_solutions(T))
    print("   Solution: %s" % T.solve())

    # T.solve() returns one solution. We need a way to access them all. Read bauhaus documentation.
    # Once we have all the solutions we can output every moveable peice and the direction it can move by outputting the i,j for when CMR, CMD, DMU, CML ho;d
   


""" SAVED FOR TROUBLESHOOTING
    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        # Ensure that you only send these functions NNF formulas
        # Literals are compiled to NNF here
        print(" %s: %.2f" % (vn, likelihood(T, v)))
    print()
"""