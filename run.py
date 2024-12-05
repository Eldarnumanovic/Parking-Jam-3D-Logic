#lucas was here
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood

# These two lines make sure a faster SAT solver is used.
from nnf import config
config.sat_backend = "kissat"


# Encoding that will store all of your constraints
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
    
class Car:
    def __init__(self, car_id, x, y, orientation):
        self.car_id = car_id
        self.x = x
        self.y = y
        self.orientation = orientation

    
    def __repr__(self):
        return f"Car({self.car_id}, x = {self.x}, y = {self.y}, orientation = {self.orientation})"
    
class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Barrier({self.x}, {self.y})"
    


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    """
    Define the constraints for the parking jam game, ensuring that the board state
    determines if all cars can escape or if any car is completely blocked.
    """
    # Constraint: A cell is empty if it contains neither a car nor a barrier
    for x in range(grid_size):
        for y in range(grid_size):
            E.add_constraint(Empty(x, y) >> (~CarAt(x, y) & ~BarrierAt(x, y)))

    for car in cars:
        if car.orientation == 'EW':
            # Escape forward (right) and backward (left) constraints for EW cars
            escape_right = And([~BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
            escape_left = And([~BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)])
            E.add_constraint(EscapeForwards(car.car_id) >> escape_right)
            E.add_constraint(EscapeBackwards(car.car_id) >> escape_left)

            # Blocked state for EW cars: Barriers on both sides
            barriers_left = And([BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)])
            barriers_right = And([BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
            fully_blocked = And(barriers_left, barriers_right)
            E.add_constraint(fully_blocked >> ~EscapeForwards(car.car_id))
            E.add_constraint(fully_blocked >> ~EscapeBackwards(car.car_id))

        elif car.orientation == 'NS':
            # Escape forward (up) and backward (down) constraints for NS cars
            escape_up = And([~BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)])
            escape_down = And([~BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
            E.add_constraint(EscapeForwards(car.car_id) >> escape_up)
            E.add_constraint(EscapeBackwards(car.car_id) >> escape_down)

            # Blocked state for NS cars: Barriers on both sides
            barriers_up = And([BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)])
            barriers_down = And([BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
            fully_blocked = And(barriers_up, barriers_down)
            E.add_constraint(fully_blocked >> ~EscapeForwards(car.car_id))
            E.add_constraint(fully_blocked >> ~EscapeBackwards(car.car_id))

    # Global Constraint: The board is a winning state if all cars can escape
    all_cars_escape = And([EscapeForwards(car.car_id) | EscapeBackwards(car.car_id) for car in cars])
    E.add_constraint(~ParkingJam() >> all_cars_escape)

    # Global Constraint: The board is a losing state if any car is completely blocked by barriers
    any_car_fully_blocked = Or([And([BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)]) &
                                 And([BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
                                 if car.orientation == 'EW'
                                 else And([BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)]) &
                                      And([BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
                                 for car in cars])
    E.add_constraint(ParkingJam() >> any_car_fully_blocked)

    return E



def is_winning_state():
    # Compile constraints
    T = example_theory()
    T = T.compile()

    # Check satisfiability
    if T.satisfiable():
        S = T.solve()
        
        print("Solution:", S)

        # Check escape conditions for all cars
        all_escaped = all(S[f"EscapeForwards({car.car_id})"] or S[f"EscapeBackwards({car.car_id})"] for car in cars)
        if all_escaped:
            print("All cars can escape!")
            return True
        else:
            print("Not all cars can escape.")
            return False
    else:
        print("No solution found. Not a winning state.")
        return False


# docker build -t parking-jam-3d .
# docker run -it --rm parking-jam-3d /bin/bash

def display_grid(grid, cars, barriers):
    """
    Display the grid with car and barrier positions.
    """
    for car in cars:
        print(f"Processing Car: ID={car.car_id}, Orientation={car.orientation}")
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            # Check if a car is at the current position
            car_at_position = next((c for c in cars if c.x == x and c.y == y), None)
            if car_at_position:
                # Directly use the orientation from the car object
                row.append(f"{car_at_position.car_id}{car_at_position.orientation}")
            elif any(b.x == x and b.y == y for b in barriers):
                # Add B for barriers
                row.append(" B ")
            else:
                # Add . for empty spaces
                row.append(" . ")
        print(" ".join(row))
    print()


def generate_random_board(size=4, num_cars=3, num_barriers=2):
    """
    Generate a random board with cars and barriers.
    """
    grid = [[0 for _ in range(size)] for _ in range(size)]
    cars = []
    barriers = []

    # Add cars
    for car_id in range(1, num_cars + 1):
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            orientation = random.choice(['NS', 'EW'])  # 0 for vertical, 1 for horizontal
            if grid[y][x] == 0:  # Empty cell
                grid[y][x] = car_id
                cars.append(Car(car_id, x, y, orientation))
                break

    # Add barriers
    for _ in range(num_barriers):
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            if grid[y][x] == 0:  # Empty cell
                grid[y][x] = -1
                barriers.append(Barrier(x, y))
                break

    return grid, cars, barriers



# Example usage
if __name__ == "__main__":
    import random

    # Define grid size
    grid_size = 4

    # Generate random board
    grid, cars, barriers = generate_random_board(size=grid_size, num_cars=3, num_barriers=4)

    # Display the initial grid
    print("Initial Grid:")
    display_grid(grid, cars, barriers)

    print(cars)
    print(barriers)

    # Define movement constraints
    #define_movement_constraints(grid_size, cars, barriers)

    # Add winnability constraints
    

    # Compile encoding
    T = example_theory()

    # Check satisfiability
    #print("Satisfiable:", T.satisfiable())
    #print("Number of solutions:", count_solutions(T))
    #print("Solution:", T.solve())
    is_winning_state()

