import math


     

def globalize_physics_vars(dihedral=0, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                cLift_a0=0.25, cL_slope=0.2, altitude=1000, cruise=52, I_roll=1000, drag_mult = 3, Constant_Altitude = False):
     # Variables
    dihedral = dihedral # positive for dihedral, negative for anhedral

    WingLength = WingLength # half the wingspan
    WingWidth = WingWidth # chord length
    BodyArea = BodyArea # for Cfside, assume the body is roughly cylindrical so this acts for vertical drag and sideslip drag
    drag_mult = drag_mult  # multiplier for drag forces

    # a_default = a_default # angle of attack in deg
    cLift_a0 = cLift_a0  # lift coefficient NACA 2414
    cL_slope = cL_slope # rise per deg
    Mass = Mass  # mass in kg

    I_roll = I_roll # moment of inertial about roll axis


    altitude = altitude  # altitude in feet up to FL400
    cruise = cruise  # cruise speed in m/s (1.94 knots = 1 m/s)

    Constant_Altitude = Constant_Altitude  # whether to adjust AoA to maintain constant altitude

    STALLANGLE = 15  # degrees

    # Constants
    R0=8.314
    cp=1005  # specific heat at constant pressure for air
    M = 0.02897  # molar mass of air
    L = -2
    g = 9.81
    rho0 = 1.225  # sea level standard density kg/m^3
    P0 = 101325  # sea level standard pressure Pa
    T0 = 288.15  # sea level standard temperature K

    cd_body = 1.1 #cylinder cross flow for high reynolds numbers

    # Calculated Constants
    #LATEX
    PA = P0 * (1+g*altitude/(cp*T0))**(-cp*M/R0)  # ambient pressure at altitude https://en.wikipedia.org/wiki/Atmospheric_pressure
    TA = T0 + (L*altitude/1000)  # ambient temperature at altitude
    rhoA = 1/((R0/M*TA)/PA)  # ambient density at altitude (ideal gas law)

    WingArea = WingLength * WingWidth * 2

    Cdbody = BodyArea * cd_body # sideslip drag coefficient, note that the whole wing does not move at the same speed


    # calculate a_default for given mass such that lift cancels weight at cruise
    a_default = (Mass*g / (2* 0.5 * rhoA * cruise**2 * (WingArea/2) * math.cos(math.pi*dihedral/180)) - cLift_a0) / cL_slope # for mass to cancel with lift
     
    _physics_vars = [
        "dihedral", "WingLength", "WingWidth", "BodyArea",
        "a_default", "cLift_a0", "cL_slope", "Mass",
        "altitude", "cruise",
        "R0", "cp", "M", "L", "g", "rho0", "P0", "T0",
        "cd_body", "Cdbody",
        "PA", "TA", "rhoA", "WingArea", "I_roll", "Cdbody", "drag_mult", "STALLANGLE", "Constant_Altitude"
    ]
     
    for _name in _physics_vars:
        globals()[_name] = locals()[_name]
    
    print("Dihedral:", dihedral)
    print("Wing Area:", WingArea)
    print("Cruise Speed:", cruise)
    print("Altitude:", altitude)
    print("AoA cruise:", a_default)


# Helper functions
def rad(theta):
    """
    Converts degrees to radians
    
    theta: angle in degrees
    """

    return theta * math.pi / 180




"""
Forces and Torques

Directions are refering to viewing head on except for left/right wing, that is pilot's view.
Right is +
Up is +
Clockwise torque is +
(rolling right from our view, rolling left from pilot's view, reduces bank angle)

Bank angle (bank) increases as the right (pilot's left) wing goes up and left wing goes down (our perspective). Opposite to torque direction.
Logic being, when bank is positive, it slips in the negative direction (to the left from our POV)

All forces are tuples (Fx, Fy)
All torques are scalars
"""


# Drag Forces

def sidedrag_F(vss):
    """
    Returns the side drag force as a tuple (Fx, Fy)
    
    vss: sideslip velocity (m/s), positive to the right from our POV
    """

    if vss < 0:
        # slipping left, so drag to the right (+)
        return (0.5 * rhoA * vss**2 * Cdbody * drag_mult, 0)
    else:
        # slipping right, so drag to the left (-)
        return (-0.5 * rhoA * vss**2 * Cdbody * drag_mult, 0)

def vertdrag_F(vy):
    """
    Returns the vertical drag force as a tuple (Fx, Fy)
    
    vy: vertical velocity (m/s), positive up from our POV
    """

    if vy < 0:
        # falling down, so drag up (+)
        return (0, 0.5 * rhoA * vy**2 * Cdbody * drag_mult)
    else:
        # going up, so drag down (-)
        return (0, -0.5 * rhoA * vy**2 * Cdbody * drag_mult)


def rotv_speed_r_l(w):
    """
    Returns the average linear vertical velocity at the right and left wing tips due to roll rate w as a tuple (vr, vl)
    
    w: roll rate in deg/s, positive is rolling left from our POV
    """

    average_lin_v = (rad(w) * WingLength / 2)*3
    return (-average_lin_v, average_lin_v)  # right wing speed, left wing speed


# Lift Forces

def leftlift_F(bank, AoA):
    """
    Returns the left wing lift force as a tuple (Fx, Fy)
    
    bank: bank angle in degrees, positive is right wing down from our POV
    AoA: angle of attack in degrees for left wing (right from our POV)
    """

    v = cruise
    cLift = cLift_a0 + cL_slope * AoA
    TotalLiftLeft = 0.5 * rhoA * v**2 * cLift * (WingArea/2)

    LiftY = TotalLiftLeft * math.cos(rad(bank)+rad(dihedral))
    # negative since with positive dihedral or positive bank, the lift points left (-)
    LiftX = -TotalLiftLeft * math.sin(rad(bank)+rad(dihedral))

    return (LiftX, LiftY)

def rightlift_F(bank, AoA):
    """
    Returns the right wing lift force as a tuple (Fx, Fy)
    
    bank: bank angle in degrees, positive is right wing down from our POV
    AoA: angle of attack in degrees for right wing (right from our POV)
    """
    v = cruise
    cLift = cLift_a0 + cL_slope * AoA
    TotalLiftRight = 0.5 * rhoA * v**2 * cLift * (WingArea/2)

    LiftY = TotalLiftRight * math.cos(rad(bank)-rad(dihedral))
    # negative since with high dihedral or positive bank, the lift points left (-)
    LiftX = -TotalLiftRight * math.sin(rad(bank)-rad(dihedral))

    return (LiftX, LiftY)

# Lift Torques

def leftlift_T(leftlift):
    """
    Returns the left wing lift torque assuming lift is in the center of the wing
    
    leftlift: left wing lift force as a tuple (Fx, Fy)
    """

    # tends to roll to our left, so negative
    return -leftlift[1] * WingLength/2

def rightlift_T(rightlift):
    """
    Returns the right wing lift torque assuming lift is in the center of the wing
    
    rightlift: right wing lift force as a tuple (Fx, Fy)
    """

    # tends to roll to our right, so positive
    return rightlift[1] * WingLength/2

# Weight Force

def weight_F():
    """
    Returns the weight force as a tuple (Fx, Fy)
    """
    return (0, -Mass * g)

# Angle Calculations

def side_slip_angle(vy, vss):
    """
    Returns the sideslip angle in degrees
    
    vy: vertical speed
    vss: sideslip speed (horizontal)
    """
    return math.degrees(math.atan2(vy, vss))

def constant_alt_angle(Fnety, bank):
    """
    Returns the angle of attack required to maintain constant altitude in degrees
    """

    AoAinc = -Fnety / (0.5 * rhoA * cruise**2 * (WingArea/2) * cL_slope * (math.cos(rad(bank)-rad(dihedral))+math.cos(rad(bank)+rad(dihedral))))
    return AoAinc

def AoAR(vss, vy, bank, w):
    """
    Returns the angle of attack for the right wing in degrees
    
    vy: vertical speed
    vss: sideslip speed (horizontal)
    bank: bank angle in degrees
    w: roll rate in deg/s
    """
    
    vsseff = -vss*math.sin(rad(bank-dihedral)) # take the component of airflow (-velocity) perpendicular to the right wing
    vy_rot = rotv_speed_r_l(w)[0]  # right wing rotational velocity
    vy = vy + vy_rot # find effective vertical speed at right wing
    vyeff = vy*math.cos(rad(bank-dihedral))
    
    # find total angle deviation from cruise deflecting in angle perpendicular to right wing
    AoAadj = math.degrees(math.atan2(vyeff+vsseff, cruise))

    # Stall condition exit case
    if ((a_default - AoAadj) > STALLANGLE) | ((a_default - AoAadj) < -STALLANGLE):
        raise ValueError("stall condition")

    return a_default - AoAadj

def AoAL(vss, vy, bank, w):
    """
    Returns the angle of attack for the left wing (right in our POV) in degrees
    
    vy: vertical speed
    vss: sideslip speed (horizontal)
    bank: bank angle in degrees
    w: roll rate in deg/s
    """

    
    vsseff = -vss*math.sin(rad(bank+dihedral)) # take the component of airflow (-velocity) perpendicular to the left wing
    vy_rot = rotv_speed_r_l(w)[1]  # left wing rotational velocity
    vy = vy + vy_rot
    vyeff = vy*math.cos(rad(bank+dihedral))
    # find total angle deviation from cruise deflecting in angle perpendicular to left wing
    AoAadj = math.degrees(math.atan2(vyeff+vsseff, cruise))

    # Stall condition
    if ((a_default - AoAadj) > 30) | ((a_default - AoAadj) < -30):
        raise ValueError("stall condition")

    return a_default - AoAadj


# Net Force and Torques

def Fnet (vss, vy, bank, w):
    """
    Returns net force as a tuple (Fx, Fy)
    
    vss: horizontal airspeed (m/s), positive to the right from our POV
    vy: vertical speed
    bank: bank angle in degrees
    w: roll rate in deg/s
    """

    weight = weight_F()[1]
    vertdrag = vertdrag_F(vy)[1]
    sidedrag = sidedrag_F(vss)[0]
    AOAL = AoAL(vss, vy, bank, w)
    AOAR = AoAR(vss, vy, bank, w)
    leftlift = leftlift_F(bank, AOAL)
    rightlift = rightlift_F(bank, AOAR)
    Fnety = weight + leftlift[1] + rightlift[1] + vertdrag

    if Constant_Altitude:
        AoAinc = constant_alt_angle(Fnety, bank)
        # print("AoAinc for constant altitude:", AoAinc)
        AOAL += AoAinc
        AOAR += AoAinc
        leftlift = leftlift_F(bank, AOAL)
        rightlift = rightlift_F(bank, AOAR)
        Fnety = weight + leftlift[1] + rightlift[1] + vertdrag

    Fnetx = sidedrag + leftlift[0] + rightlift[0]
    return (Fnetx, Fnety)


def Tnet (vss, vy, bank, w):
    """
    Returns net torque in Nm

    vss: horizontal airspeed (m/s), positive to the right from our POV
    vy: vertical speed
    bank: bank angle in degrees
    w: roll rate in deg/s
    """

    left_T = leftlift_T(leftlift_F(bank, AoAL(vss, vy, bank, w)))
    right_T = rightlift_T(rightlift_F(bank, AoAR(vss, vy, bank, w)))
    return left_T + right_T


if __name__ == "__main__":
    # NOT THE MAIN SIMULATION (see Simulator_Main.py)
    # For testing physics engine and debugging.
    globalize_physics_vars(dihedral=0, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                       cLift_a0=0.25, cL_slope=0.2,
                                       altitude=1000, cruise=52, I_roll=1000, drag_mult = 1, Constant_Altitude = True)

    # simple test
    bank = 15  # degrees counter clockwise    _o/
    vy = 0  # m/s down
    vss = 0 # m/s slipping 
    w = 5  # deg/s
    print("a_default" + ": ", a_default)
    
    #    _o/    slipping <- and falling v
    print("AoAR:", AoAR(vss,vy,bank, w))
    print("AoAL:", AoAL(vss,vy,bank, w))
    print("Fnetx:", Fnet(vss, vy, bank, w)[0])
    print("Fnety:", Fnet(vss, vy, bank, w)[1])
    print("Tnet:", Tnet(vss, vy, bank, w))