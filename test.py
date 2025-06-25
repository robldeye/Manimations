import numpy as np
from sympy import Matrix

A_mat = Matrix([
    [0.3, 0.1],
    [0.2, 0.4]
])
eigenvalues = []
eigenvectors = []
for value, mult, vector in A_mat.eigenvects():
    eigenvectors.extend(vector)

v1_0 = np.array([1, 1])
minEvecs = []
for vector in eigenvectors:
    minEvec = vector / vector[np.argmin(np.abs(vector))] # make smallest entry 1
    minEvecs.append(minEvec)

Evec_mat = Matrix.hstack(*minEvecs)
sol_coeffs = Evec_mat.inv() @ v1_0

print(minEvecs)
print(Evec_mat)

