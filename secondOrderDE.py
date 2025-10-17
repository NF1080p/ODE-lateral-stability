import numpy as np
import matplotlib.pyplot as plt


def second_order_DE(y0, yprime0, a, b, c, f_t, steps, endval):
    """
    Solves second order differential equation of form ay'' + by' + c = f(t)
    Args:
        y0 (float): initial condition for y
        yprime0 (float): initial condition for y'
        a (float): coefficient of y''
        b (float): coefficient of y'
        c (float): coefficient of y
        steps (int): number of time steps
        endval (int): simulate upto t = endval
    """
    # generate t for plotting
    t = np.linspace(0, endval, steps)
    y = np.zeros(len(t))
    dy = np.zeros(len(t))
    y[0] = y0
    dy[0] = yprime0 

    for n in range(0, len(t)-1):
        dt = t[n+1]-t[n] # we could play with variable time intervals
        # euler's method: 
        y[n+1] = y[n] + dy[n]*dt
        dy[n+1] = dy[n] + (f_t[n]-b*dy[n]-c*y[n])*dt/a

    return y

def plot_solution(y, steps, endval):
    t = np.linspace(0, endval, steps)
    plt.plot(t, y)
    plt.title("a cool title here")
    plt.show()
       
# test case 
y0 = 1; v0 = 0;
endval = 2*np.pi; steps = 100
f_t = np.zeros(steps)
output = second_order_DE(y0, v0, 1, 0, 1, f_t, steps, endval)
plot_solution(output, steps, endval)

    # todo:
    #  - implement a runga kutta algo 
    #  - vectorize it so it works for linear systems


