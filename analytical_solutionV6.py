from sympy import symbols, Function, Eq, dsolve, latex, lambdify, Symbol, solve
import matplotlib.pyplot as plt
import physics
import grapher
import numpy as np
from scipy.integrate import odeint

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

# Define initial conditions
x_0 = 10           # initial position
x_dot_0 = 0.0      # initial velocity
y_0 = 10           # initial position
y_dot_0 = 0.0      # initial velocity
bank_0 = np.pi/6   # initial bank angle
bank_dot_0 = 0     # initial bank rate

# Define system as coupled ODEs for numerical solving
# State vector: [x, x_dot, y, y_dot, bank, bank_dot]
def system_positive(state, t):
    x, x_dot, y, y_dot, bank, bank_dot = state
    
    # d2x/dt2 = -(-2*C_1*bank + 4*C_2*x_dot*b0*dihedral)/Mass
    x_ddot = -(-2*C_1*bank + 4*C_2*x_dot*b0*dihedral) / physics.Mass
    
    # d2y/dt2 = (-Mass*g + 2*(C_1 - C_2*x_dot*bank)/Mass)
    y_ddot = (-physics.Mass*physics.g + 2*(C_1 - C_2*x_dot*bank)) / physics.Mass
    
    # d2bank/dt2 = (WingLength*0.5*C_2*x_dot*dihedral - 0.5*rhoA*bank_dot*WingArea*WingLength^2)/I_roll
    bank_ddot = (physics.WingLength*0.5*C_2*x_dot*dihedral - 0.5*physics.rhoA*bank_dot*physics.WingArea*physics.WingLength**2 - 0.3*bank) / physics.I_roll
    
    return [x_dot, x_ddot, y_dot, y_ddot, bank_dot, bank_ddot]

def system_negative(state, t):
    x, x_dot, y, y_dot, bank, bank_dot = state
    
    # d2x/dt2 = -(-2*C_1*bank + 4*C_2*x_dot*b0*(-dihedral))/Mass
    x_ddot = -(-2*C_1*bank + 4*C_2*x_dot*b0*(-dihedral)) / physics.Mass
    
    # d2y/dt2 = (-Mass*g + 2*(C_1 - C_2*x_dot*bank)/Mass)
    y_ddot = (-physics.Mass*physics.g + 2*(C_1 - C_2*x_dot*bank)) / physics.Mass
    
    # d2bank/dt2 = (WingLength*0.5*C_2*x_dot*(-dihedral) - 0.5*rhoA*bank_dot*WingArea*WingLength^2)/I_roll
    bank_ddot = (physics.WingLength*0.5*C_2*x_dot*(-dihedral) - 0.5*physics.rhoA*bank_dot*physics.WingArea*physics.WingLength**2) / physics.I_roll
    
    return [x_dot, x_ddot, y_dot, y_ddot, bank_dot, bank_ddot]

# Initial state
initial_state = [x_0, x_dot_0, y_0, y_dot_0, bank_0, bank_dot_0]

# Time array
t_list = np.linspace(0, 10, 1000)

# Solve numerically
print("Solving system numerically...")
solution_positive = odeint(system_positive, initial_state, t_list)
solution_negative = odeint(system_negative, initial_state, t_list)

# Extract results
x_list = solution_positive[:, 0]
y_list = solution_positive[:, 2]
bank_list = solution_positive[:, 4]

x_list_neg = solution_negative[:, 0]
y_list_neg = solution_negative[:, 2]
bank_list_neg = solution_negative[:, 4]

grapher.plot_solution_more_params(x_list, t_list, title="analytical solution - x vs t",  ylabel="horizontal position (m)")
grapher.plot_solution_more_params(y_list, t_list, title="analytical solution - y vs t", ylabel="vertical position (m)")
grapher.plot_solution_more_params(bank_list, t_list, title="dihedral analytical solution - bank vs t", ylabel="bank angle (rad)")
grapher.plot_solution_more_params(bank_list_neg, t_list, title="anhedral analytical solution - bank vs t", ylabel="bank angle (rad)")
plt.show()