"""
Analytical solution for lateral stability aircraft motion. 
Uses sympy to solve linearized equations of motion.
Version 5. Graphs used in report generated in this file
"""
from sympy import symbols, Function, Eq, dsolve, latex, lambdify, Symbol
import matplotlib.pyplot as plt
import archive.physics_backup as physics
import grapher
import numpy as np

plt.rcParams.update({'font.size': 14}) # make plot font size bigger


# variables
t = symbols('t')
x = Function('x')
y = Function('y')
bank = Function('bank')

"""
2nd order ODE system
"""

# constants from physics engine

c_1 = physics.cLift_a0 + physics.cL_slope * (physics.a_default - 1)
c_2 = physics.cL_slope / physics.cruise

multiplier = 0.25 * physics.rhoA * physics.cruise**2 * physics.WingLength

C_1 = c_1 * multiplier
C_2 = c_2 * multiplier

dihedral = 5 
b0 = 0.2

net_x_og = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*bank(t)*dihedral)/physics.Mass)
net_x_decoupled = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*b0*dihedral)/physics.Mass)
net_x_decoupled_neg = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*b0*(-dihedral))/physics.Mass)

net_y_og = Eq(y(t).diff(t,2), (-physics.Mass*physics.g+2*(C_1 - C_2*x(t).diff(t)*bank(t))/physics.Mass))

net_bank_old = Eq(bank(t).diff(t,2), (physics.WingLength*0.5*C_2*x(t).diff(t) - 0.5*physics.rhoA*bank(t).diff(t)*physics.WingArea*physics.WingLength**2)/physics.I_roll)  

net_bank = Eq(bank(t).diff(t,2), (physics.WingLength*0.5*C_2*x(t).diff(t)*dihedral - 0.5*physics.rhoA*bank(t).diff(t)*physics.WingArea*physics.WingLength**2)/physics.I_roll)  

general_solution_positive_dihedral = dsolve([net_x_decoupled, net_y_og, net_bank])
general_solution_negative_dihedral = dsolve([net_x_decoupled_neg, net_y_og, net_bank])

# Extract equations from sympy dsolve general solution
x_eqn = general_solution_positive_dihedral[0].rhs
x_eqn_neg = general_solution_negative_dihedral[0].rhs
y_eqn = general_solution_positive_dihedral[1].rhs
y_eqn_neg = general_solution_negative_dihedral[1].rhs
bank_eqn = general_solution_positive_dihedral[2].rhs
bank_eqn_neg = general_solution_negative_dihedral[2].rhs

# General solutions has 6 integration constants defined below.
C1, C2, C3, C4, C5, C6 = symbols('C1 C2 C3 C4 C5 C6')

# Integration constants to set initial conditions
# v6 of this code specifies initial conditions

integration_constants_dihedral = {
    C1: 1e6,
    C2: 0.0,
    C3: 1e2,
    C4: 0.0,
    C5: 0.0,
    C6: 0.0
}
integration_constants_anhedral = {
    C1: 5e4,
    C2: -5e4,
    C3: 1e1,
    C4: -1e1,
    C5: 1e-2,
    C6: -1e-2
}

integration_constants = integration_constants_dihedral

x_specific = x_eqn.subs(integration_constants)
y_specific = y_eqn.subs(integration_constants)
bank_specific = bank_eqn.subs(integration_constants)

x_specific_neg = x_eqn_neg.subs(integration_constants)
y_specific_neg = y_eqn_neg.subs(integration_constants)
bank_specific_neg = bank_eqn_neg.subs(integration_constants)

# convert to numpy functions !!!
x_numpy = lambdify(t, x_specific, "numpy")
y_numpy = lambdify(t, y_specific, "numpy")
bank_numpy = lambdify(t, bank_specific, "numpy")

x_numpy_neg = lambdify(t, x_specific_neg, "numpy")
y_numpy_neg = lambdify(t, y_specific_neg, "numpy")
bank_numpy_neg = lambdify(t, bank_specific_neg, "numpy")

# print out LaTeX equation output
print("Equations formatted in LaTeX:")
#print("bank(t) DIHEDRAL = {}".format(latex(bank_specific)))
print("bank(t) ANHEDRAL = {}".format(latex(bank_specific_neg)))


# plot
t_list = np.linspace(0, 13, 1000) # lambda function are cool. it can compute x_numpy for an arbitrary size of t_list :O
x_list = x_numpy(t_list)
y_list = y_numpy(t_list)
bank_list = bank_numpy(t_list) / 250 # since integration constants were chosen to give the best visual, scale it down to give realistic initial conditions. 

x_list_neg = x_numpy_neg(t_list)
y_list_neg = y_numpy_neg(t_list)
bank_list_neg = bank_numpy_neg(t_list) / 85000

grapher.plot_solution_more_params(x_list, t_list, title="analytical solution - x vs t",  ylabel="horizontal position (m)")
grapher.plot_solution_more_params(y_list, t_list, title="analytical solution - y vs t", ylabel="vertical position (m)")
grapher.plot_solution_more_params(bank_list, t_list, title="Dihedral Analytical Solution - Bank vs time", ylabel="bank angle (rad)")
grapher.plot_solution_more_params(bank_list_neg, t_list, title="Anhedral Analytical Solution - Bank vs time", ylabel="bank angle (rad)")
plt.show()