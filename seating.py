from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions

from nnf import config
config.sat_backend = "kissat"

# Initialize the encoding
E = Encoding()

# Define propositions
@proposition(E)
class NextTo:
    def __init__(self, person1, person2):
        """
        Represents whether person1 is sitting next to person2.
        """
        self.person1 = person1
        self.person2 = person2

    def _prop_name(self):
        return f"NextTo({self.person1}, {self.person2})"


# Add constraints
# Rule 1: Alice and Bob cannot sit next to each other
E.add_constraint(~NextTo("Alice", "Bob"))

# Rule 2: Charlie must sit next to Alice
E.add_constraint(NextTo("Charlie", "Alice"))

# Compile the encoding
T = E.compile()

# Check satisfiability
if T.satisfiable():
    print("The seating arrangement is satisfiable!")
    solution = T.solve()
    print("Solution:", solution)
    print("Number of solutions:", count_solutions(T))
else:
    print("No valid seating arrangement exists.")
