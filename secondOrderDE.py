import numpy as np
import matplotlib.pyplot as plt
import physics


def second_order_DE(y0, yprime0, a, b, c, f_t, steps, endval):
    """
    Solves second order differential equation of form ay'' + by' + cy = f(t)
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

def second_order_DE_nonlinear(y0, yprime0, steps, endval):
    """
    Solves second order differential equation of form ay'' + by'|y'| + c = 0 
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
    x = np.zeros(len(t))
    dy = np.zeros(len(t))
    dx = np.zeros(len(t))
    # initial conditions
    y[0] = y0
    dy[0] = yprime0 

    for n in range(0, len(t)-1):
        dt = t[n+1]-t[n] # we could play with variable time intervals
        # euler's method: 
        #ddy = -physics.g -0.5/physics.Mass * physics.rhoA * physics.cd_body * abs(dy[n])*dy[n] + physics.leftlift_F(physics.bank, physics.a_default)[1]/physics.Mass + physics.rightlift_F(physics.bank, physics.a_default)[1]/physics.Mass
        ddy = -physics.g -0.5/physics.Mass * physics.rhoA * physics.cd_body * abs(dy[n])*dy[n] + physics.leftlift_F(0.005, physics.a_default)[1]/physics.Mass + physics.rightlift_F(5, physics.a_default)[1]/physics.Mass

        #ddx = (1/physics.Mass) * physics.Fnetx(physics.vss, physics.vy, physics.bank) #tempp
        ddx = (1/physics.Mass) * physics.Fnetx(0.001, 0.001, 5)

        # y update
        y[n+1] = y[n] + dy[n]*dt
        dy[n+1] = dy[n] + ddy*dt

        # x update
        x[n+1] = x[n] + dx[n]*dt
        dx[n+1] = dx[n] + ddx*dt
        
    return (x, y) 

    
def second_order_RK_simple_case(y, yprime, steps, endval):
    # https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html
    # https://lpsa.swarthmore.edu/NumInt/NumIntFourth.html
    def func(t, x, v): # f(t,x,v) = mt + kx + lx'
        m = 1
        k = 1
        l = 0.1
        return -k*x-l*v
    def rhs(t,x,v):
        # might want to vary by a constant
        return func(t,x,v)
    def g(v):
        return v # first order term
    def testing(t,x,v,h):
        k0 = h*g(v)
        l0 = h*rhs(t,x,v)

        k1 = h*g(v+0.5*l0)
        l1 = h*rhs(t+0.5*h, x+0.5*k0, v+0.5*10)

        k2 = h*g(v+0.5*l1)
        l2 = h*rhs(t + 0.5*h, x+0.5*k1, v+0.5*l1)

        k3 = h*g(v+l2)
        l3 = h*rhs(t+0.5*h, x+0.5*k2, v+0.5*l2)

        x_next = x+ (1/6)*(k0 + 2*k1 + 2*k2 + k3)
        y_next = x+ (1/6)*(00 + 2*l1 + 2*l2 + l3)

        return (x_next, y_next)


    

def plot_solution(y, steps, endval):
    t = np.linspace(0, endval, steps)
    plt.plot(t, y)
    plt.title("a cool title here")
    plt.show()
       

if __name__ == "__main__":
    # test case 
    y0 = 1; v0 = 0
    endval = 2*np.pi; steps = 100
    f_t = np.zeros(steps)
    output = second_order_DE(y0, v0, 1, 0, 1, f_t, steps, endval)
    plot_solution(output, steps, endval)

        # todo:
        #  - implement a runga kutta algo 
        #  - vectorize it so it works for linear systems


