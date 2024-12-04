#lucas was here
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"


# Encoding that will store all of your constraints
E = Encoding()

CAR_ORIENTATIONS = [0, 1] #0 for NS, 1 for EW


CAR_LOCATIONS = []
BARRIER_LOCATIONS = []
LOCATION_GRID = {}


# To create propositions, create classes for them first, annotated with "@proposition" and the Encoding
@proposition(E)
class BasicPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"


# Different classes for propositions are useful because this allows for more dynamic constraint creation
# for propositions within that class. For example, you can enforce that "at least one" of the propositions
# that are instances of this class must be true by using a @constraint decorator.
# other options include: at most one, exactly one, at most k, and implies all.
# For a complete module reference, see https://bauhaus.readthedocs.io/en/latest/bauhaus.html
@constraint.at_least_one(E)
@proposition(E)
class FancyPropositions:

    def __init__(self, data):
        self.data = data

    def _prop_name(self):
        return f"A.{self.data}"

# Call your variables whatever you want
a = BasicPropositions("a")
b = BasicPropositions("b")   
c = BasicPropositions("c")
d = BasicPropositions("d")
e = BasicPropositions("e")
# At least one of these will be true
x = FancyPropositions("x")
y = FancyPropositions("y")
z = FancyPropositions("z")


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



# Example usage
if __name__ == "__main__":
    # Create a 4x4 grid
    parking_lot = Grid(size=4)
    
    # Randomize cars and barriers
    parking_lot.randomize(num_cars=5, num_barriers=3)
    
    # Display the grid
    print("Initial Grid State:")
    parking_lot.display()



from bauhaus import Encoding, proposition, constraint, And, Or, Not

# Initialize encoding
E = Encoding()

# Define Propositions
@proposition(E)
class Orientation:
    def __init__(self, car_id, direction):
        """
        Represents the orientation of a car.
        direction: 'NS' for North/South or 'EW' for East/West
        """
        self.car_id = car_id
        self.direction = direction

    def _prop_name(self):
        return f"Orientation({self.car_id},{self.direction})"


@proposition(E)
class CarAt:
    def __init__(self, x, y):
        """
        Represents whether a car is at a specific location (x, y).
        """
        self.x = x
        self.y = y

    def _prop_name(self):
        return f"CarAt({self.x},{self.y})"


@proposition(E)
class BarrierAt:
    def __init__(self, x, y):
        """
        Represents whether a barrier is at a specific location (x, y).
        """
        self.x = x
        self.y = y

    def _prop_name(self):
        return f"BarrierAt({self.x},{self.y})"


# Constraints
@proposition(E)
class Empty:
    def __init__(self, x, y):
        """
        Represents whether a location (x, y) is empty.
        """
        self.x = x
        self.y = y

    def _prop_name(self):
        return f"Empty({self.x},{self.y})"


@proposition(E)
class EscapeForwards:
    def __init__(self, car_id):
        """
        Represents whether a car can escape forwards.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"EscapeForwards({self.car_id})"


@proposition(E)
class EscapeBackwards:
    def __init__(self, car_id):
        """
        Represents whether a car can escape backwards.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"EscapeBackwards({self.car_id})"


@proposition(E)
class BarrierAhead:
    def __init__(self, car_id):
        """
        Represents whether there is a barrier directly ahead of a car.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"BarrierAhead({self.car_id})"


@proposition(E)
class BarrierBehind:
    def __init__(self, car_id):
        """
        Represents whether there is a barrier directly behind a car.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"BarrierBehind({self.car_id})"


@proposition(E)
class CarAhead:
    def __init__(self, car_id):
        """
        Represents whether there is a car directly ahead of a car.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"CarAhead({self.car_id})"


@proposition(E)
class CarBehind:
    def __init__(self, car_id):
        """
        Represents whether there is a car directly behind a car.
        """
        self.car_id = car_id

    def _prop_name(self):
        return f"CarBehind({self.car_id})"


@proposition(E)
class ParkingJam:
    def __init__(self):
        """
        Represents whether the entire grid is in a parking jam state.
        """
        pass

    def _prop_name(self):
        return "ParkingJam"


# Define Constraints
def define_constraints(grid_size, cars, barriers):
    """
    Add constraints for the game based on the provided propositions.
    """
    for x in range(grid_size):
        for y in range(grid_size):
            # A cell is empty if it contains neither a car nor a barrier
            E.add_constraint(
                Empty(x, y) >> (~CarAt(x, y) & ~BarrierAt(x, y))
            )

    for car in cars:
        # Escape constraints for forwards and backwards
        E.add_constraint(
            EscapeForwards(car.car_id) >> And(
                [Empty(car.x + i, car.y) for i in range(1, grid_size - car.x)]
                if car.orientation == 'EW'
                else [Empty(car.x, car.y - i) for i in range(1, car.y + 1)]
            )
        )
        E.add_constraint(
            EscapeBackwards(car.car_id) >> And(
                [Empty(car.x - i, car.y) for i in range(1, car.x + 1)]
                if car.orientation == 'EW'
                else [Empty(car.x, car.y + i) for i in range(1, grid_size - car.y)]
            )
        )

        # Barrier constraints
        E.add_constraint(
            BarrierAhead(car.car_id) >> Or(
                [BarrierAt(car.x + 1, car.y)]
                if car.orientation == 'EW'
                else [BarrierAt(car.x, car.y - 1)]
            )
        )
        E.add_constraint(
            BarrierBehind(car.car_id) >> Or(
                [BarrierAt(car.x - 1, car.y)]
                if car.orientation == 'EW'
                else [BarrierAt(car.x, car.y + 1)]
            )
        )

        # Car constraints
        E.add_constraint(
            CarAhead(car.car_id) >> Or(
                [CarAt(car.x + 1, car.y)]
                if car.orientation == 'EW'
                else [CarAt(car.x, car.y - 1)]
            )
        )
        E.add_constraint(
            CarBehind(car.car_id) >> Or(
                [CarAt(car.x - 1, car.y)]
                if car.orientation == 'EW'
                else [CarAt(car.x, car.y + 1)]
            )
        )

    # Parking Jam constraint
    E.add_constraint(
        ParkingJam() >> Or(
            [BarrierAhead(car.car_id) & BarrierBehind(car.car_id) for car in cars]
        )
    )


# Example Usage
if __name__ == "__main__":
    grid_size = 4
    cars = [
        {"car_id": 1, "x": 1, "y": 1, "orientation": "EW"},
        {"car_id": 2, "x": 2, "y": 3, "orientation": "NS"},
    ]
    barriers = [
        {"x": 0, "y": 1},
        {"x": 3, "y": 2},
    ]

    define_constraints(grid_size, cars, barriers)

    # Compile encoding
    T = E.compile()

    # Check satisfiability
    print("Satisfiable:", T.satisfiable())
    print("Number of solutions:", count_solutions(T))
    print("Solution:", T.solve())