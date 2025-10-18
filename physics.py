import math



# Variables
dihedral = 0 # positive for dihedral, negative for anhedral


WingLength = 3 # half the wingspan
WingWidth = 1 # chord length
BodyArea = 5 # for Cfside

a_default = 2 # angle of attack in deg
CLift_a = 0.25  # lift coefficient NACA 2414
CL_slope = 0.2 # rise per deg
Mass = 1000  # mass in kg



altitude = 1000  # altitude in feet up to FL400
cruise = 50  # cruise speed in m/s (1.94 knots = 1 m/s)



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
cd_wingperp = 1 #flat plate perpendicular to flow

# Calculated Constants
#LATEX
PA = P0 * (1+g*altitude/(cp*T0))**(-cp*M/R0)  # ambient pressure at altitude https://en.wikipedia.org/wiki/Atmospheric_pressure
TA = T0 + (L*altitude/1000)  # ambient temperature at altitude
rhoA = 1/((R0/M*TA)/PA)  # ambient density at altitude (ideal gas law)

WingArea = WingLength * WingWidth * 2 # for Cfrot

Cdside = BodyArea * cd_body # sideslip drag coefficient, note that the whole wing does not move at the same speed

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

Bank angle (bank) increases as the right wing goes up and left wing goes down (our perspective)

All forces are tuples (Fx, Fy)
All torques are scalars
"""

# Drag Forces
def sidedrag_F(vss):
    return (0.5 * rhoA * vss**2 * Cdside, 0)

def vertdrag_F(vy):
    return (0, 0.5 * rhoA * vy**2 * cd_wingperp * (WingArea))


#Drag Torque
def rotdrag_T(w): #LATEX
    #integral of F (prop to v^2) over the lever arm (increases linearly)
    unitlengthdrag = 0.5 * rhoA * (w**2) * cd_wingperp * WingWidth
    LeverLength = WingLength*WingLength / 2  # triangle: integral of length from 0 to WingLength
    return unitlengthdrag * LeverLength


# Lift Forces

def leftlift_F(bank, AoA=a_default):
    # right from our POV
    v = cruise
    CLift = CLift_a + CL_slope * AoA
    TotalLiftLeft = 0.5 * rhoA * v**2 * CLift * (WingArea/2)

    LiftY = TotalLiftLeft * math.cos(rad(dihedral)+rad(bank))
    LiftX = TotalLiftLeft * math.sin(rad(dihedral)+rad(bank))

    return (LiftX, LiftY)

def rightlift_F(bank, AoA=a_default):
    # left from our POV
    v = cruise
    CLift = CLift_a + CL_slope * AoA
    TotalLiftRight = 0.5 * rhoA * v**2 * CLift * (WingArea/2)

    LiftY = TotalLiftRight * math.cos(rad(dihedral)-rad(bank))
    LiftX = TotalLiftRight * math.sin(rad(dihedral)-rad(bank))

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
    return math.degrees(math.atan2(vy, vss))

def AoAR(b, bank):
    hor = vss
    vert = vy

    return a_default - b * math.cos(rad(bank))