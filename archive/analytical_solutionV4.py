from sympy import symbols, Function, Eq, dsolve, latex, lambdify, Symbol
import matplotlib.pyplot as plt
import physics
import grapher
import numpy as np

# variables
t = symbols('t')
x = Function('x')
y = Function('y')
bank = Function('bank')

"""
2nd order ODE system
"""

# constants
# from physics engine

c_1 = physics.cLift_a0 + physics.cL_slope * (physics.a_default - 1)
c_2 = physics.cL_slope / physics.cruise

multiplier = 0.25 * physics.rhoA * physics.cruise**2 * physics.WingLength

C_1 = c_1 * multiplier
C_2 = c_2 * multiplier

# use _og equations

net_x_og = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*bank(t)*physics.dihedral)/physics.Mass)
net_x = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 0*4*C_2*x(t).diff(t)*bank(t)*physics.dihedral)/physics.Mass)

net_y_og = Eq(y(t).diff(t,2), (-physics.Mass*physics.g+2*(C_1 - C_2*x(t).diff(t)*bank(t))/physics.Mass))
net_y = Eq(y(t).diff(t,2), (-physics.Mass*physics.g+2*(C_1 - 0*C_2*x(t).diff(t)*bank(t))/physics.Mass))

net_bank = Eq(bank(t).diff(t,2), (physics.WingLength*0.5*C_2*x(t).diff(t) - 0.5*physics.rhoA*bank(t).diff(t)*physics.WingArea*physics.WingLength**2)/physics.I_roll)  

# solve without ICs to get general solution
general_solution = dsolve([net_x_og, net_y_og, net_bank])

#print("General Solution:")
#for yippie in general_solution:
    #print(f"{yippie}")

x_eqn = general_solution[0].rhs
y_eqn = general_solution[1].rhs
bank_eqn = general_solution[2].rhs

# general solutions has 6 integration constants. define them.

C1, C2, C3, C4, C5, C6 = symbols('C1 C2 C3 C4 C5 C6')

integration_constants = {
    C1: 1.0e6,    # Very strong roll moment response (increased order of magnitude)
    C2: -1.0e6,   # Increased coupling between roll and lateral motion (stronger influence)
    C3: 1.0e4,    # Increased frequency (faster oscillations)
    C4: -1.0e2,   # Reduced damping (more sustained oscillations)
    C5: -1.0e2,   # Further reduced damping (more oscillatory behavior)
    C6: 1.0e3     # Amplify the initial perturbation or response
}

x_specific = x_eqn.subs(integration_constants)
y_specific = y_eqn.subs(integration_constants)
bank_specific = bank_eqn.subs(integration_constants)

# convert to numpy functions !!!
x_numpy = lambdify(t, x_specific, "numpy")
y_numpy = lambdify(t, y_specific, "numpy")
bank_numpy = lambdify(t, bank_specific, "numpy")

# plot
t_list = np.linspace(0, 20, 1000) # lambda function are cool. it can compute x_numpy for an arbitrary size of t_list :O
x_list = x_numpy(t_list)
y_list = y_numpy(t_list)
bank_list = bank_numpy(t_list)

grapher.plot_solution(x_list, t_list, title="analytical solution - x vs t")
grapher.plot_solution(y_list, t_list, title="analytical solution - y vs t")
grapher.plot_solution(bank_list, t_list, title="analytical solution - bank vs t")
plt.show()