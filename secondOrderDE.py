import numpy as np
import physics
import keyboardctrl as kb


def nick_test(x, y, bank, dx, dy, dbank, dt):

    Fnety = physics.Fnety(dx, dy, bank)
    ya =(1/physics.Mass) * Fnety
    
    Fnetx = physics.Fnetx(dx, dy, bank)
    xa = (1/physics.Mass) * Fnetx # inputs to Fnetx are vss, vy, bank

    ba = -(1/physics.I_roll) * physics.Tnet(dx, dy, bank, dbank) # inputs to Tnet are vss, vy, bank, w

    x1 = x + (dx)*dt
    dx1 = dx + xa*dt
    y1 = y + (dy)*dt
    dy1 = dy + ya*dt
    bank1 = bank + (dbank)*dt
    dbank1 = dbank + ba*dt

    return(x1, y1, bank1, dx1, dy1, dbank1)

    
def second_order_DE_nonlinear_rk4_one_step(x, y, bank, dx, dy, dbank, dt):
    # derivative functions to handle different inputs easy
    def f_dy(dy):
        return dy
    def f_ddy(dy, bank):
        Fnety = physics.Fnety(dx, dy, bank, dbank)
        return (1/physics.Mass) * Fnety
    
    def f_dx(dx):
        return dx 
    
    def f_ddx(dx, dy, bank):
        Fnetx = physics.Fnetx(dx, dy, bank, dbank)
        return (1/physics.Mass) * Fnetx # inputs to Fnetx are vss, vy, bank
    
    def f_dbank(dbank):
        return dbank
    
    def f_ddbank(dx, dy, bank, dbank):
        return -(1/physics.I_roll) * inject_aileron_control(dx, dy, bank, dbank) # inputs to Tnet are vss, vy, bank, w

    def inject_aileron_control(dx, dy, bank, dbank):
        T_natural = physics.Tnet(dx, dy, bank, dbank)

        ap(kb.ap_on)

        T_input = kb.aileron_input * -300
        print(T_natural, T_input)
        return T_natural + T_input
    
    def ap(ap_on):
        if ap_on:
            if (bank < -0.01 and kb.aileron_input < 30) or (bank > 0.01 and kb.aileron_input > -30):
                kb.aileron_input -= bank/5 + dbank/3
            else:
                kb.aileron_input = 0


    
    #rk4 !!!

    # y substeps

    k1_y = dt * f_dy(dy)
    k1_dy = dt * f_ddy(dy, bank)
    
    k2_y = dt * f_dy(dy + 0.5*k1_dy)
    k2_dy = dt * f_ddy(dy + 0.5*k1_dy, bank + 0.5*dt*dbank)
    
    k3_y = dt * f_dy(dy + 0.5*k2_dy)
    k3_dy = dt * f_ddy(dy + 0.5*k2_dy, bank + 0.5*dt*dbank)
    
    k4_y = dt * f_dy(dy + k3_dy)
    k4_dy = dt * f_ddy(dy + k3_dy, bank + dt*dbank)
    
    # x substeps
    
    k1_x = dt * f_dx(dx)
    k1_dx = dt * f_ddx(dx, dy, bank)
    
    k2_x = dt * f_dx(dx + 0.5*k1_dx)
    k2_dx = dt * f_ddx(dx + 0.5*k1_dx, dy + 0.5*k1_dy, bank + 0.5*dt*dbank)
    
    k3_x = dt * f_dx(dx + 0.5*k2_dx)
    k3_dx = dt * f_ddx(dx + 0.5*k2_dx, dy + 0.5*k2_dy, bank + 0.5*dt*dbank)
    
    k4_x = dt * f_dx(dx + k3_dx)
    k4_dx = dt * f_ddx(dx + k3_dx, dy + k3_dy, bank + dt*dbank)
    
    # bank substeps
    
    k1_bank = dt * f_dbank(dbank)
    k1_dbank = dt * f_ddbank(dx, dy, bank, dbank)
    
    k2_bank = dt * f_dbank(dbank + 0.5*k1_dbank)
    k2_dbank = dt * f_ddbank(dx + 0.5*k1_dx, dy + 0.5*k1_dy, 
                            bank + 0.5*k1_bank, dbank + 0.5*k1_dbank)
    
    k3_bank = dt * f_dbank(dbank + 0.5*k2_dbank)
    k3_dbank = dt * f_ddbank(dx + 0.5*k2_dx, dy + 0.5*k2_dy, 
                            bank + 0.5*k2_bank, dbank + 0.5*k2_dbank)
    
    k4_bank = dt * f_dbank(dbank + k3_dbank)
    k4_dbank = dt * f_ddbank(dx + k3_dx, dy + k3_dy, 
                            bank + k3_bank, dbank + k3_dbank)
    
    # Update all variables
    y1 = y + (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
    dy1 = dy + (k1_dy + 2*k2_dy + 2*k3_dy + k4_dy) / 6
    
    x1 = x + (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
    dx1 = dx + (k1_dx + 2*k2_dx + 2*k3_dx + k4_dx) / 6
    
    bank1 = bank + (k1_bank + 2*k2_bank + 2*k3_bank + k4_bank) / 6
    dbank1 = dbank + (k1_dbank + 2*k2_dbank + 2*k3_dbank + k4_dbank) / 6

    #print(f"dy1: {dy1}, dx1: {dx1}, dbank1: {dbank1}")
    return (x1, y1, bank1, dx1, dy1, dbank1)

def second_order_DE_nonlinear_rk4(y0, yprime0, x0, xprime0, bank0, bankprime0, steps, endval):
    """
    DEPRECIATED CODE
    Euler's method to solve second order DE for lateral aircraft motion
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
    lent = len(t)+5
    y = np.zeros(lent)
    x = np.zeros(lent)
    bank = np.zeros(lent)
    dy = np.zeros(lent)
    dx = np.zeros(lent)
    dbank = np.zeros(lent)
    # initial conditions
    y[0] = y0
    dy[0] = yprime0
    x[0] = x0
    dx[0] = xprime0
    bank[0] = bank0
    dbank[0] = bankprime0

    # derivative functions to handle different inputs easy
    def f_dy(dy):
        return dy
    def f_ddy(dy, bank):
        return -physics.g -0.5/physics.Mass * physics.rhoA * physics.cd_body * abs(dy)*dy + physics.leftlift_F(bank, physics.a_default)[1]/physics.Mass + physics.rightlift_F(bank, physics.a_default)[1]/physics.Mass
    
    def f_dx(dx):
        return dx 
    
    def f_ddx(dx, dy, bank):
        return (1/physics.Mass) * physics.Fnetx(dx, dy, bank) # inputs to Fnetx are vss, vy, bank
    
    def f_dbank(dbank):
        return dbank
    
    def f_ddbank(dx, dy, bank, dbank):
        return (1/physics.I_roll) * physics.Tnet(dx, dy, bank, dbank) # inputs to Tnet are vss, vy, bank, w

    for n in range(0, len(t)-1):
        dt = t[n+1]-t[n] # we could play with variable time intervals

        #rk4 !!!

        # y substeps

        k1_y = dt * f_dy(dy[n])
        k1_dy = dt * f_ddy(dy[n], bank[n])
        
        k2_y = dt * f_dy(dy[n] + 0.5*k1_dy)
        k2_dy = dt * f_ddy(dy[n] + 0.5*k1_dy, bank[n] + 0.5*dt*dbank[n])
        
        k3_y = dt * f_dy(dy[n] + 0.5*k2_dy)
        k3_dy = dt * f_ddy(dy[n] + 0.5*k2_dy, bank[n] + 0.5*dt*dbank[n])
        
        k4_y = dt * f_dy(dy[n] + k3_dy)
        k4_dy = dt * f_ddy(dy[n] + k3_dy, bank[n] + dt*dbank[n])
        
        # x substeps
        
        k1_x = dt * f_dx(dx[n])
        k1_dx = dt * f_ddx(dx[n], dy[n], bank[n])
        
        k2_x = dt * f_dx(dx[n] + 0.5*k1_dx)
        k2_dx = dt * f_ddx(dx[n] + 0.5*k1_dx, dy[n] + 0.5*k1_dy, bank[n] + 0.5*dt*dbank[n])
        
        k3_x = dt * f_dx(dx[n] + 0.5*k2_dx)
        k3_dx = dt * f_ddx(dx[n] + 0.5*k2_dx, dy[n] + 0.5*k2_dy, bank[n] + 0.5*dt*dbank[n])
        
        k4_x = dt * f_dx(dx[n] + k3_dx)
        k4_dx = dt * f_ddx(dx[n] + k3_dx, dy[n] + k3_dy, bank[n] + dt*dbank[n])
        
        # bank substeps
        
        k1_bank = dt * f_dbank(dbank[n])
        k1_dbank = dt * f_ddbank(dx[n], dy[n], bank[n], dbank[n])
        
        k2_bank = dt * f_dbank(dbank[n] + 0.5*k1_dbank)
        k2_dbank = dt * f_ddbank(dx[n] + 0.5*k1_dx, dy[n] + 0.5*k1_dy, 
                                bank[n] + 0.5*k1_bank, dbank[n] + 0.5*k1_dbank)
        
        k3_bank = dt * f_dbank(dbank[n] + 0.5*k2_dbank)
        k3_dbank = dt * f_ddbank(dx[n] + 0.5*k2_dx, dy[n] + 0.5*k2_dy, 
                                bank[n] + 0.5*k2_bank, dbank[n] + 0.5*k2_dbank)
        
        k4_bank = dt * f_dbank(dbank[n] + k3_dbank)
        k4_dbank = dt * f_ddbank(dx[n] + k3_dx, dy[n] + k3_dy, 
                                bank[n] + k3_bank, dbank[n] + k3_dbank)
        
        # Update all variables
        y[n+1] = y[n] + (k1_y + 2*k2_y + 2*k3_y + k4_y) / 6
        dy[n+1] = dy[n] + (k1_dy + 2*k2_dy + 2*k3_dy + k4_dy) / 6
        
        x[n+1] = x[n] + (k1_x + 2*k2_x + 2*k3_x + k4_x) / 6
        dx[n+1] = dx[n] + (k1_dx + 2*k2_dx + 2*k3_dx + k4_dx) / 6
        
        bank[n+1] = bank[n] + (k1_bank + 2*k2_bank + 2*k3_bank + k4_bank) / 6
        dbank[n+1] = dbank[n] + (k1_dbank + 2*k2_dbank + 2*k3_dbank + k4_dbank) / 6

    return (x, y, bank)

def second_order_DE_nonlinear(y0, yprime0, x0, xprime0, bank0, bankprime0, steps, endval):
    """
    DEPRECIATED CODE
    Euler's method to solve second order DE for lateral aircraft motion
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
    lent = len(t)+5
    y = np.zeros(lent)
    x = np.zeros(lent)
    bank = np.zeros(lent)
    dy = np.zeros(lent)
    dx = np.zeros(lent)
    dbank = np.zeros(lent)
    # initial conditions
    y[0] = y0/20
    dy[0] = yprime0
    x[0] = x0/20
    dx[0] = xprime0
    bank[0] = bank0
    dbank[0] = bankprime0

    for n in range(0, len(t)-1):
        dt = t[n+1]-t[n] # we could play with variable time intervals
        # euler's method: 
        ddy = -physics.g -0.5/physics.Mass * physics.rhoA * physics.cd_body * abs(dy[n])*dy[n] + physics.leftlift_F(bank[n], physics.a_default)[1]/physics.Mass + physics.rightlift_F(bank[n], physics.a_default)[1]/physics.Mass

        ddx = (1/physics.Mass) * physics.Fnetx(dx[n], dy[n], bank[n]) # inputs to Fnetx are vss, vy, bank

        ddbank = (1/physics.I_roll) * physics.Tnet(dx[n], dy[n], bank[n], dbank[n]) # inputs to Tnet are vss, vy, bank, w

        # y update
        y[n+1] = y[n] + dy[n]*dt
        dy[n+1] = dy[n] + ddy*dt

        # x update
        x[n+1] = x[n] + dx[n]*dt
        dx[n+1] = dx[n] + ddx*dt

        # bank update
        bank[n+1] = bank[n] + dbank[n]*dt
        dbank[n+1] = dbank[n] + ddbank*dt

    return (x, y, bank)

def second_order_DE(y0, yprime0, a, b, c, f_t, steps, endval):
    """
    DEPRECIATED CODE
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