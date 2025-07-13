import numpy as np

# Base class for handling general linear systems
class LinearSystem:
    def __init__(self, coefficients, constants):
        self.coefficients = np.array(coefficients)
        self.constants = np.array(constants)

    def solve(self):
        try:
            return np.linalg.solve(self.coefficients, self.constants)
        except np.linalg.LinAlgError as error:
            return f"Error solving the system: {error}"

# Subclass specific to 3-variable systems
class ThreeVariableSystem(LinearSystem):
    def __init__(self, coefficients, constants):
        if len(coefficients) != 3 or len(coefficients[0]) != 3:
            raise ValueError("Only 3x3 systems are supported.")
        super().__init__(coefficients, constants)

    def show_equations(self):
        variables = ['x', 'y', 'z']
        for row, result in zip(self.coefficients, self.constants):
            equation = ' + '.join(f"{coef}{var}" for coef, var in zip(row, variables))
            print(f"{equation} = {result}")

# Run the solver
if __name__ == "__main__":
    # Define the system: Ax = b
    c:\Users\Farid\AppData\Local\Packages\Microsoft.ScreenSketch_8wekyb3d8bbwe\TempState\Recordings\20250424-1800-33.6729325.mp4
    b = [1, 2, 3]

    system = ThreeVariableSystem(A, b)
    
    print("Solving the following system of equations:")
    system.show_equations()
    print("\nSolution:")
    
    solution = system.solve()
    if isinstance(solution, str):
        print(solution)
    else:
        print(f"x = {solution[0]}")
        print(f"y = {solution[1]}")
        print(f"z = {solution[2]}")
