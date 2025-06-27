import numpy as np
from sympy import Matrix, Rational, latex
from scipy.integrate import odeint
from scipy.interpolate import interp1d

locations = []
bound = 4

for x in np.arange(0, bound+1):
    for y in np.arange(0, 2*bound+1):
        locations.append([x, y])

# define ODE
r = 3
K = 5
def model(y, t):
    return r * (1 - y / K) * y

# solving ODE for multiple solution paths
np.random.seed(42)
num_solutions = 4
initial_values = np.random.uniform(0, 2*bound - 1, num_solutions)
t = np.linspace(0, 5, 100) # smoothness of curve later on tied to framerate in manim.cfg, not step size

# some functions for making direction field arrows
def dir(y, t):
    return np.array([1, model(y, t)])

def unit(v):
    if np.linalg.norm(v) != 0:
        return v/np.linalg.norm(v)
    else:
        return v


interpolated_solutions = []
for i, vec in enumerate(initial_values):
    solution = odeint(model, vec, t)
    interpolated_solution = interp1d(t, solution, axis=0, kind='linear')
    interpolated_solutions.append(interpolated_solution)

print(len(interpolated_solutions))

for solution in interpolated_solutions:
    for t in np.arange(0, 5):
        print(interpolated_solution(t))

