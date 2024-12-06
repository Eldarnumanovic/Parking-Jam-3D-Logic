from bauhaus import *
from bauhaus.utils import *


# Initialize encoding
E = Encoding()

DIRECTIONS = ['NS','EW']
               
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

"""
# Define Constraints
def define_constraints(grid_size, cars, barriers):
    
    #Add constraints for the game based on the provided propositions.
    
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
"""


def display_grid(grid, cars, barriers):
    """
    Display the grid with car and barrier positions.
    """
    for y in range(len(grid)):
        row = []
        for x in range(len(grid[0])):
            if any(c.x == x and c.y == y for c in cars):
                row.append("C")
            elif any(b.x == x and b.y == y for b in barriers):
                row.append("B")
            else:
                row.append(".")
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
            orientation = random.choice([0, 1])  # 0 for vertical, 1 for horizontal
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
    #T = E.compile()

    # Check satisfiability
    #print("Satisfiable:", T.satisfiable())
    #print("Number of solutions:", count_solutions(T))
    #print("Solution:", T.solve())





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

    #define_constraints(grid_size, cars, barriers)

    # Compile encoding
    #T = E.compile()

    # Check satisfiability
    #print("Satisfiable:", T.satisfiable())
    #print("Number of solutions:", count_solutions(T))
    #print("Solution:", T.solve())
