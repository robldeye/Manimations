import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d
        
a = 1
b = 0
c = 1 

def sode(y, t):
    y, z = y
    dydt = [z, 1/a*(-b*z - c*y)] #[y', y'']
    return dydt

t = np.linspace(0, 10, 100)
y_0 = 2
z_0 = 2
initcond = [y_0, z_0]
sol = odeint(sode, initcond, t)
interp_sol = interp1d(t, sol, axis=0, kind='linear')

print(interp_sol)