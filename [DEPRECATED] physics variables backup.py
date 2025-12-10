import math

# Variables
dihedral = 0 # positive for dihedral, negative for anhedral

I_roll = 1000 # moment of inertial about roll axis

WingLength = 4 # half the wingspan
WingWidth = 1 # chord length
BodyArea = 5 # for Cfside, assume the body is roughly cylindrical so this acts for vertical drag and sideslip drag
drag_mult = 1.0  # multiplier for drag forces

a_default = 4 # angle of attack in deg
cLift_a0 = 0.25  # lift coefficient NACA 2414
cL_slope = 0.2 # rise per deg
Mass = 1000  # mass in kg



altitude = 1000  # altitude in feet up to FL400
cruise = 52  # cruise speed in m/s (1.94 knots = 1 m/s)



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

a_default = (Mass*g / (2* 0.5 * rhoA * cruise**2 * (WingArea/2) * math.cos(math.pi*dihedral/180)) - cLift_a0) / cL_slope # for mass to cancel with lift