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

dihedral = 15
dihedral = dihedral * (np.pi / 180)  # convert to radians
b0 = 0
#prime:
#dihedral = 5
#b0 = 0.2

net_x_og = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*bank(t)*dihedral)/physics.Mass)

net_x_decoupled = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*b0*dihedral)/physics.Mass)
net_x_decoupled_neg = Eq(x(t).diff(t,2), -(-2*C_1*bank(t) + 4*C_2*x(t).diff(t)*b0*(-dihedral))/physics.Mass)

net_y_og = Eq(y(t).diff(t,2), (-physics.Mass*physics.g+2*(C_1 - C_2*x(t).diff(t)*bank(t))/physics.Mass))

net_bank_old = Eq(bank(t).diff(t,2), (physics.WingLength*0.5*C_2*x(t).diff(t) - 0.5*physics.rhoA*bank(t).diff(t)*physics.WingArea*physics.WingLength**2)/physics.I_roll)  

k = 0.03   # choose a realistic value

#net_bank = Eq(
    #bank(t).diff(t,2),
    #-k * bank(t)
    #- (0.5*physics.rhoA*physics.WingArea*physics.WingLength**2/physics.I_roll) * bank(t).diff(t)
    #+ (physics.WingLength*0.5*C_2/physics.I_roll)*x(t).diff(t)
#)
net_bank = Eq(bank(t).diff(t,2), (physics.WingLength*0.5*C_2*x(t).diff(t)*dihedral - 0.5*physics.rhoA*bank(t).diff(t)*physics.WingArea*physics.WingLength**2)/physics.I_roll)  

# Instead of solving without ICs and then guessing constants:
ics = {
    x(0): 10,           # initial position
    x(t).diff(t).subs(t, 0): 0.0,  # initial velocity
    y(0): 10,
    y(t).diff(t).subs(t, 0): 0.0,
    bank(0): np.pi/9,
    bank(t).diff(t).subs(t, 0): 0
}

general_solution_positive_dihedral = dsolve([net_x_decoupled, net_y_og, net_bank], ics=ics)
general_solution_negative_dihedral = dsolve([net_x_decoupled_neg, net_y_og, net_bank], ics=ics)

x_eqn = general_solution_positive_dihedral[0].rhs
x_eqn_neg = general_solution_negative_dihedral[0].rhs
y_eqn = general_solution_positive_dihedral[1].rhs
y_eqn_neg = general_solution_negative_dihedral[1].rhs
bank_eqn = general_solution_positive_dihedral[2].rhs
bank_eqn_neg = general_solution_negative_dihedral[2].rhs

print(general_solution_negative_dihedral)

# general solutions has 3 integration constants. define them.
C1, C2, C3, C4 = symbols('C1 C2 C3 C4')

integration_constants = {
    C1: 0,
    C2: 1.0,
    C3: 1.0,
    C4: 1.0
}
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

# plot
t_list = np.linspace(0, 30, 1000) # lambda function are cool. it can compute x_numpy for an arbitrary size of t_list :O
x_list = x_numpy(t_list)
y_list = y_numpy(t_list)
bank_list = bank_numpy(t_list)

x_list_neg = x_numpy_neg(t_list)
y_list_neg = y_numpy_neg(t_list)
bank_list_neg = bank_numpy_neg(t_list)

grapher.plot_solution_more_params(x_list, t_list, title="analytical solution - x vs t",  ylabel="horizontal position (m)")
grapher.plot_solution_more_params(y_list, t_list, title="analytical solution - y vs t", ylabel="vertical position (m)")
grapher.plot_solution_more_params(bank_list, t_list, title="dihedral analytical solution - bank vs t", ylabel="bank angle (rad)")
grapher.plot_solution_more_params(bank_list_neg, t_list, title="anhedral analytical solution - bank vs t", ylabel="bank angle (rad)")
plt.show()