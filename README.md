# ODE-lateral-stability

This repo contains code for our MAT292 Final Project. 


Our goal was to explore how passive aircraft geometry and active autopilots are used in maintaining stable flight during cruise conditions. Our product is a two dimensional lateral stability aircraft simulation with a working autopilot. The most important files and their description are included below. 

<div align="center">

| File name | Description |
| ------- | ---- |
| Simulator_Main.py | Aircraft simulation user interface |
| physics.py | The simulation physics engine. Contains equations of motion and values of constants |
| secondOrderDE.py | Solves second order differential equations numerically. Used to generate the aircraft flight path |
| analytical_solutionV5.py | Solves linearized equations of motion to obtain an analytical approximation of the aircraft behaviour |
| grapher.py | Graphs bank angle, horizontal position, and vertical position of the aircraft flight data from simulation |
| keyboardctrl.py | Let's the user toggle autopilot and manual aileron control |

</div>

## Installation

Our code is written in Python3. To reproduce our results, please ensure you have Python3.8+ Then:

1. Clone this repository
2. Create and activate virtual environment in Python
3. Install the dependendencies: `pip install pyglet numpy pynput matplotlib sympy`.


Alternative (No virtual environment)


&nbsp;&nbsp;&nbsp;&nbsp;1a. Clone this repository\
&nbsp;&nbsp;&nbsp;&nbsp;2a. Ensure `math`, `matplotlib`, `numpy`, `os`, `pynput`, `sympy`, and `pyglet` are installed via `pip install` commands\
&nbsp;&nbsp;&nbsp;&nbsp;3a. Open the repository directory in a python environment (vscode)

4. Set the desired initial variables in the `__init__` function of Simulator_Main.py
5. Variables are preset with defaults and recommended variables are described in full
    in comments above the call to `globalize_physics_vars()`. To start the sim with autopilot engaged, toggle change the input `Autopilot` to `True` (`Autopilot=True`). By default, the sim starts with autopilot off.  
6. To run the sim, run `python Simulator_Main.py` in your terminal. A GUI will pop up showing the aircraft motion. 
7. Enjoy the visual display of lateral stability/instabililty.
8. To use manual control, run the simulation as normal, and type 'A' or 'D' into the terminal to bank left and right respectively.
9. To use the autopilot, run the simulation as normal, and type 'P' into the terminal. Note that manual control is disabled if autopilot is active.
10. The terminal should acknowledge the input and will attempt to stabilize the aircraft.
11. In some cases of anhedral, stabilization may be impossible if the autopilot is activated too late.
12. Once satisfied, end the sim by closing the GUI. The sim will end automatically if the aircaft hits one of its failure conditions

This generates a file called `data-SIM_START_DATE_AND_TIME.txt` in the folder `./data/`. This file is formatted as:

    horizontal position (m)     vertical position (m)     bank angle (deg)    time (s) 
    
13. To plot this data, run `python grapher.py`. The most recent set of data will be plotted.

