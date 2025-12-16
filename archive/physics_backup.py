import math


     

def globalize_physics_vars(dihedral=0, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                cLift_a0=0.25, cL_slope=0.2, altitude=1000, cruise=52, I_roll=1000, drag_mult = 3):
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



    # Constants
    R0=8.314
    cp=1005  # specific heat at constant pressure for air
    M = 0.02897  # molar mass of air
    L = -2
    g = 9.81
    rho0 = 1.225  # sea level standard density kg/m^3
    P0 = 101325  # sea level standard pressure Pa
    T0 = 288.15  # sea level standard temperature K

    cd_body = 0.47 #sphere

    # Calculated Constants
    #LATEX
    PA = P0 * (1+g*altitude/(cp*T0))**(-cp*M/R0)  # ambient pressure at altitude https://en.wikipedia.org/wiki/Atmospheric_pressure
    TA = T0 + (L*altitude/1000)  # ambient temperature at altitude
    rhoA = 1/((R0/M*TA)/PA)  # ambient density at altitude (ideal gas law)

    WingArea = WingLength * WingWidth * 2 # for Cfrot

    Cdbody = BodyArea * cd_body # sideslip drag coefficient, note that the whole wing does not move at the same speed


    # calculate a_default for given mass such that lift cancels weight at cruise
    a_default = (Mass*g / (2* 0.5 * rhoA * cruise**2 * (WingArea/2) * math.cos(math.pi*dihedral/180)) - cLift_a0) / cL_slope # for mass to cancel with lift
     
    _physics_vars = [
        "dihedral", "WingLength", "WingWidth", "BodyArea",
        "a_default", "cLift_a0", "cL_slope", "Mass",
        "altitude", "cruise",
        "R0", "cp", "M", "L", "g", "rho0", "P0", "T0",
        "cd_body", "Cdbody",
        "PA", "TA", "rhoA", "WingArea", "I_roll", "Cdbody", "drag_mult"
    ]
     
    for _name in _physics_vars:
        globals()[_name] = locals()[_name]
    
    print("Dihedral:", dihedral)
    print("Wing Area:", WingArea)
    print("Cruise Speed:", cruise)
    print("Altitude:", altitude)
    print("AoA cruise:", a_default)

# assumptions, pressure does not change much with slight altitude changes

# Helper functions
def rad(theta):
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
    if vss < 0:
        # slipping left, so drag to the right (+)
        return (0.5 * rhoA * vss**2 * Cdbody * drag_mult, 0)
    else:
        # slipping right, so drag to the left (-)
        return (-0.5 * rhoA * vss**2 * Cdbody * drag_mult, 0)

def vertdrag_F(vy):
    if vy < 0:
        # falling down, so drag up (+)
        return (0, 0.5 * rhoA * vy**2 * Cdbody * drag_mult)
    else:
        # going up, so drag down (-)
        return (0, -0.5 * rhoA * vy**2 * Cdbody * drag_mult)


#Drag Torque
# def rotdrag_T(w): #CHANGE TO AFFECT AOA
#     #integral of F (prop to v^2) over the lever arm (increases linearly)
#     average_lin_v = rad(w) * WingLength / 2  # average linear velocity of the wing
#     unitlengthdrag = 0.5 * rhoA * (average_lin_v)**2 * WingArea
#     LeverLength = WingLength*WingLength / 2  # triangle: integral of length from 0 to WingLength
#     return -unitlengthdrag * LeverLength * drag_mult

def rotv_speed_r_l(w):
    average_lin_v = (rad(w) * WingLength / 2)*3
    return (-average_lin_v, average_lin_v)  # right wing speed, left wing speed


# Lift Forces

def leftlift_F(bank, AoA):
    # right from our POV
    v = cruise
    cLift = cLift_a0 + cL_slope * AoA
    TotalLiftLeft = 0.5 * rhoA * v**2 * cLift * (WingArea/2)

    LiftY = TotalLiftLeft * math.cos(rad(bank)+rad(dihedral))
    # negative since with positive dihedral or positive bank, the lift points left (-)
    LiftX = -TotalLiftLeft * math.sin(rad(bank)+rad(dihedral))

    return (LiftX, LiftY)

def rightlift_F(bank, AoA):
    # left from our POV
    v = cruise
    cLift = cLift_a0 + cL_slope * AoA
    TotalLiftRight = 0.5 * rhoA * v**2 * cLift * (WingArea/2)

    LiftY = TotalLiftRight * math.cos(rad(bank)-rad(dihedral))
    # negative since with high dihedral or positive bank, the lift points left (-)
    LiftX = -TotalLiftRight * math.sin(rad(bank)-rad(dihedral))

    return (LiftX, LiftY)

# Lift Torques

def leftlift_T(leftlift):
    # assumes lift is in the center of the wing
    # tends to roll to our left, so negative
    return -leftlift[1] * WingLength/2

def rightlift_T(rightlift):
    # assumes lift is in the center of the wing
    # tends to roll to our right, so positive
    return rightlift[1] * WingLength/2

# Weight Force
def weight_F():
    return (0, -Mass * g)

# Angle Calculations

def side_slip_angle(vy, vss):
    #b
    # we dont really care about sideslip angle since we are breaking it up into vvert and vss
    return math.degrees(math.atan2(vy, vss))

def AoAR(vss, vy, bank, w):
    # take the component of airflow (-velocity) perpendicular to the right wing
    vsseff = -vss*math.sin(rad(bank-dihedral))
    vy_rot = rotv_speed_r_l(w)[0]  # right wing rotational velocity
    vy = vy + vy_rot
    vyeff = vy*math.cos(rad(bank-dihedral))
    
    # find total angle deviation from cruise deflecting in angle perpendicular to right wing
    AoAadj = math.degrees(math.atan2(vyeff+vsseff, cruise))

    # Stall condition
    if ((a_default - AoAadj) > 15) | ((a_default - AoAadj) < -15):
        raise ValueError("stall condition")

    return a_default - AoAadj

def AoAL(vss, vy, bank, w):
    # take the component of airflow (-velocity) perpendicular to the left wing

    vsseff = -vss*math.sin(rad(bank+dihedral))
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

def Fnety (vss, vy, bank, w):
    weight = weight_F()[1]
    vertdrag = vertdrag_F(vy)[1]
    leftlift = leftlift_F(bank, AoAL(vss, vy, bank, w))[1]
    rightlift = rightlift_F(bank, AoAR(vss, vy, bank, w))[1]

    return weight + leftlift + rightlift + vertdrag

def Fnetx (vss, vy, bank, w):
    sidedrag = sidedrag_F(vss)[0]
    leftlift = leftlift_F(bank, AoAL(vss, vy, bank, w))[0]
    rightlift = rightlift_F(bank, AoAR(vss, vy, bank, w))[0]

    return sidedrag + leftlift + rightlift

def Tnet (vss, vy, bank, w):
    left_T = leftlift_T(leftlift_F(bank, AoAL(vss, vy, bank, w)))
    right_T = rightlift_T(rightlift_F(bank, AoAR(vss, vy, bank, w)))
    return left_T + right_T


if __name__ == "__main__":

    # NOT THE MAIN SIMULATION
    # For testing physics engine and debugging.
    globalize_physics_vars(dihedral=0, Mass=1000, WingLength=4, WingWidth=1, BodyArea=5,
                                       cLift_a0=0.25, cL_slope=0.2,
                                       altitude=1000, cruise=52, I_roll=1000)

    # simple test
    bank = 15  # degrees counter clockwise    _o/
    vy = 0  # m/s down
    vss = 0 # m/s slipping 
    w = 5  # deg/s
    print("a_default" + ": ", a_default)
    
    #    _o/    slipping <- and falling v
    print("AoAR:", AoAR(vss,vy,bank, w))
    print("AoAL:", AoAL(vss,vy,bank, w))
    print("Fnetx:", Fnetx(vss, vy, bank, w))
    print("Fnety:", Fnety(vss, vy, bank, w))
    print("Tnet:", Tnet(vss, vy, bank, w))