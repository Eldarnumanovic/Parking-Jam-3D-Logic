from bauhaus import Encoding, proposition, constraint, And, Or

from examples import examples

 
from nnf import config
config.sat_backend = "kissat"



E = Encoding()


# Define Propositions
@proposition(E)
class Orientation:
    def __init__(self, car_id, direction):
        """
        Represents the orientation of a car.
        direction: 'NS' for North/South or 'EW' for East/West
        N is always forwards for NS cars, E is forwards for EW Cars
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


def example_theory(grid_size, cars):
    """
    Define the constraints for the parking jam game, ensuring that the board state
    determines if all cars can escape or if any car is completely blocked.
    """
    # Constraint: A cell is empty if it contains neither a car nor a barrier
    for x in range(grid_size):
        for y in range(grid_size):
            E.add_constraint(Empty(x, y) >> (~CarAt(x, y) & ~BarrierAt(x, y)))


    # loop through cars list and add constraints for each one
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
    any_car_blocked = Or([And([
        And([BarrierAt(car.x - i, car.y) for i in range(1, car.x + 1)]),
        And([BarrierAt(car.x + i, car.y) for i in range(1, grid_size - car.x)])
    ]) if car.orientation == "EW" else And([
        And([BarrierAt(car.x, car.y - i) for i in range(1, car.y + 1)]),
        And([BarrierAt(car.x, car.y + i) for i in range(1, grid_size - car.y)])
    ]) for car in cars])

    E.add_constraint(all_cars_escape)
    E.add_constraint(~any_car_blocked)

    return E



def is_winning_state(grid_size, cars, barriers):
    # Compile constraints
    T = example_theory(grid_size, cars)
    T = T.compile()

    # Check satisfiability
    if T.satisfiable():
        S = T.solve()
       
        print("\nBarrier States:")
        for barrier in barriers:
            barrier_at = S.get(BarrierAt(barrier.x, barrier.y), "Unknown")
            print(f"Barrier at ({barrier.x}, {barrier.y}): {barrier_at}")

        # Check if all cars can escape
        all_escaped = all(S.get(EscapeForwards(car.car_id), False) or S.get(EscapeBackwards(car.car_id), False) for car in cars)
        if all_escaped:
            print("All cars can escape!\n")
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


def generate_set_board(size, car_list, barrier_list):
    """
    Generate a board with a set list of cars and barriers, and tie it to the propositions.
    """
    global cars, barriers
    grid = [[0 for _ in range(size)] for _ in range(size)]
    cars = []
    barriers = []

    # Add cars from the provided car list
    for car_data in car_list:
        car_id, x, y, orientation = car_data
        if grid[y][x] == 0:  # Ensure the cell is empty
            grid[y][x] = car_id
            new_car = Car(car_id, x, y, orientation)
            cars.append(new_car)
            
            # Add the car's position and orientation to the encoding
            E.add_constraint(CarAt(x, y))
            E.add_constraint(Orientation(car_id, orientation))

    # Add barriers from the provided barrier list
    for barrier_data in barrier_list:
        x, y = barrier_data
        if grid[y][x] == 0:  # Ensure the cell is empty
            grid[y][x] = -1
            new_barrier = Barrier(x, y)
            barriers.append(new_barrier)
            

            # Add the barrier's position to the encoding
            E.add_constraint(BarrierAt(x, y))

    return grid, cars, barriers



def generate_random_board(size, num_cars, num_barriers):
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

def display_solution(grid, cars, barriers, grid_size):
    """
    Display the solution of the game, showing step-by-step how cars escape the grid.
    """
    iteration = 0
    while cars:
        print(f"Iteration {iteration}:")
        display_grid(grid, cars, barriers)

        escaping_car = None
        escape_direction = None

        for car in cars:
            can_escape_forwards = True
            can_escape_backwards = True

            # Check forward and backward paths based on orientation
            if car.orientation == 'EW':
                # Check forward (right)
                for i in range(1, grid_size - car.x):
                    if any(b.x == car.x + i and b.y == car.y for b in barriers):
                        can_escape_forwards = False
                        break
                    if any(c.x == car.x + i and c.y == car.y for c in cars):
                        can_escape_forwards = False
                        break

                # Check backward (left)
                for i in range(1, car.x + 1):
                    if any(b.x == car.x - i and b.y == car.y for b in barriers):
                        can_escape_backwards = False
                        break
                    if any(c.x == car.x - i and c.y == car.y for c in cars):
                        can_escape_backwards = False
                        break

            elif car.orientation == 'NS':
                # Check forward (up)
                for i in range(1, car.y + 1):
                    if any(b.x == car.x and b.y == car.y - i for b in barriers):
                        can_escape_forwards = False
                        break
                    if any(c.x == car.x and c.y == car.y - i for c in cars):
                        can_escape_forwards = False
                        break

                # Check backward (down)
                for i in range(1, grid_size - car.y):
                    if any(b.x == car.x and b.y == car.y + i for b in barriers):
                        can_escape_backwards = False
                        break
                    if any(c.x == car.x and c.y == car.y + i for c in cars):
                        can_escape_backwards = False
                        break

            # If a car can escape, choose the direction and break the loop
            if can_escape_forwards:
                escaping_car = car
                escape_direction = "forwards"
                break
            elif can_escape_backwards:
                escaping_car = car
                escape_direction = "backwards"
                break

        # If no car can escape, it's a losing state
        if not escaping_car:
            print("No car can escape. This is not a winning state.")
            return

        # Remove the escaping car from the grid and update propositions
        print(f"Car {escaping_car.car_id} has exited {escape_direction}.\n")
        cars.remove(escaping_car)
        for x in range(grid_size):
            for y in range(grid_size):
                if grid[y][x] == escaping_car.car_id:
                    grid[y][x] = 0  # Mark the cell as empty

        iteration += 1

    # Print final message only once after all cars have exited
    print("All cars have escaped! Winning state achieved.")


if __name__ == "__main__":
    import random

    def main():
            
            # Uncomment this to use randomly generated grids
            """
            # Prompt user for grid size, number of cars, and barriers
            grid_size = 10  # You can adjust this as needed
            num_cars = 13  # Number of cars
            num_barriers = 13  # Number of barriers

            if ((num_cars + num_barriers)>grid_size**2):
                return ("Not enough spaces on grid for cars and barriers")

            # Generate random grid
            grid, cars, barriers = generate_random_board(size=grid_size, num_cars=num_cars, num_barriers=num_barriers)
            """


            # Select an example by changing this variable manually
            example_number = 3  # Change this number to 1 - 10

            # Fetch the selected example
            selected_example = examples[example_number - 1]

            # Extract data from the selected example
            grid_size = selected_example["size"]
            car_list = selected_example["car_list"]
            barrier_list = selected_example["barrier_list"]

            # Call the generate_set_board function with the selected example's data
            grid, cars, barriers = generate_set_board(grid_size, car_list, barrier_list)




            # Display the generated grid
            print("Initial Grid:")
            display_grid(grid, cars, barriers)

            # Check if the generated grid is winnable
            if is_winning_state(grid_size, cars, barriers):
                # Display the solution if winnable
                display_solution(grid, cars, barriers, grid_size)
            else:
                print("This state is not winnable.")

                
    # Run the main function
    main()