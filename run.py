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

@proposition(E)
class Car:
    def __init__(self, car_id, x, y, orientation):
        self.car_id = car_id
        self.x = x
        self.y = y
        self.orientation = orientation

    
    def _prop_name(self):
        return f"Car({self.car_id}, x = {self.x}, y = {self.y}, orientation = {self.orientation})"

@proposition(E)
class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _prop_name(self):
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
            # Escape constraints for EW cars
            escape_right = And([~BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
            escape_left = And([~BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)])
            E.add_constraint(EscapeForwards(car.car_id) >> escape_right)
            E.add_constraint(EscapeBackwards(car.car_id) >> escape_left)

            # Fully blocked state for EW cars
            barriers_left = And([BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)])
            barriers_right = And([BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
            fully_blocked_by_barriers = And(barriers_left, barriers_right)
            E.add_constraint(fully_blocked_by_barriers >> ~EscapeForwards(car.car_id))
            E.add_constraint(fully_blocked_by_barriers >> ~EscapeBackwards(car.car_id))

        elif car.orientation == 'NS':
            # Escape constraints for NS cars
            escape_up = And([~BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)])
            escape_down = And([~BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
            E.add_constraint(EscapeForwards(car.car_id) >> escape_up)
            E.add_constraint(EscapeBackwards(car.car_id) >> escape_down)

            # Fully blocked state for NS cars
            barriers_up = And([BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)])
            barriers_down = And([BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
            fully_blocked_by_barriers = And(barriers_up, barriers_down)
            E.add_constraint(fully_blocked_by_barriers >> ~EscapeForwards(car.car_id))
            E.add_constraint(fully_blocked_by_barriers >> ~EscapeBackwards(car.car_id))

    # Define a winning state: All cars can escape
    all_cars_escape = And([EscapeForwards(car.car_id) | EscapeBackwards(car.car_id) for car in cars])

    # Define a losing state: Any car is blocked on both sides by barriers
    any_car_blocked = Or([
        And([
            And([BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)]),
            And([BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
        ]) if car.orientation == "EW" else And([
            And([BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)]),
            And([BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
        ]) for car in cars
    ])

    E.add_constraint(all_cars_escape)
    E.add_constraint(~any_car_blocked)

    return E



def is_winning_state():
    # Compile constraints
    T = example_theory()
    T = T.compile()

    # Check satisfiability
    if T.satisfiable():
        S = T.solve()
        print("\nSAT Solver Solution:")
        print("Escape Forward/Backward and Blocked States:")
        for car in cars:
            escape_forward = S.get(EscapeForwards(car.car_id), "Unknown")
            escape_backward = S.get(EscapeBackwards(car.car_id), "Unknown")
            car_at = S.get(CarAt(car.x, car.y), "Unknown")
            print(f"Car {car.car_id}: Escape Forward: {escape_forward}, Escape Backward: {escape_backward}, CarAt: {car_at}")

        print("\nBarrier States:")
        for barrier in barriers:
            barrier_at = S.get(BarrierAt(barrier.x, barrier.y), "Unknown")
            print(f"Barrier at ({barrier.x}, {barrier.y}): {barrier_at}")

        # Check if all cars can escape
        all_escaped = all(S.get(EscapeForwards(car.car_id), False) or S.get(EscapeBackwards(car.car_id), False) for car in cars)
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
    Generate a random board with cars and barriers, and tie it to the propositions.
    """
    global cars, barriers
    grid = [[0 for _ in range(size)] for _ in range(size)]
    cars = []
    barriers = []

    # Add cars
    for car_id in range(1, num_cars + 1):
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            orientation = random.choice(['NS', 'EW'])
            if grid[y][x] == 0:  # Empty cell
                grid[y][x] = car_id
                cars.append(Car(car_id, x, y, orientation))

                # Add the car's position to the encoding
                E.add_constraint(CarAt(x, y))
                E.add_constraint(Orientation(car_id, orientation))
                break

    # Add barriers
    for _ in range(num_barriers):
        while True:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            if grid[y][x] == 0:  # Empty cell
                grid[y][x] = -1
                barriers.append(Barrier(x, y))

                # Add the barrier's position to the encoding
                E.add_constraint(BarrierAt(x, y))
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
    display_grid(grid, cars, barriers)# One car at (1,1) facing EW, Barriers block left and right
    is_winning_state()

    # Define movement constraints
    #define_movement_constraints(grid_size, cars, barriers)
    """
    # Add winnability constraints
    T = example_theory()
    T = T.compile()



    if T.satisfiable():
        print("The board is solvable!")
        # Get the solution
        S = T.solve()
    
    # Print propositions related to barriers and cars
    else:
        print("The board is not solvable!")  

    for car in cars:
        print(f"Car {car.car_id}:")
        print(f"  EscapeForwards: {S[EscapeForwards(car.car_id)]}")
        print(f"  EscapeBackwards: {S[EscapeBackwards(car.car_id)]}")
    
    for car in cars:
        print(f"CarAt({car.x}, {car.y}): {S[CarAt(car.x, car.y)]}")
    # Check individual barriers
    for barrier in barriers:
            print(f"BarrierAt({barrier.x}, {barrier.y}): {S[BarrierAt(barrier.x, barrier.y)]}")
    

    # Compile encoding
    T = example_theory()

    # Check satisfiability
    #print("Satisfiable:", T.satisfiable())
    #print("Number of solutions:", count_solutions(T))
    #print("Solution:", T.solve())
    is_winning_state()
"""
