# ODE-lateral-stability

This repo contains code for our MAT292 Final Project. We created a simulation to help analyze lateral stability in an aircraft. 

(copy paste shortened version of our intro here)



## Installation

Our code is written in Python3. To reproduce our results, start by installing the dependencies.

1. Clone this repository
2. Create and activate virtual environment in Python
3. Install the dependendencies: `pip install pyglet numpy pynput matplotlib sympy`

Alternative (No virtual environment)

1a. Clone this repository
2a. Ensure python 3, math, matplotlib, numpy, os, pynput, sympy, and pyglet are installed via 'pip install' commands
3a. Open the repository directory in a python environment (vscode)

4. Set the desired initial variables in the __init__ function of Simulator_Main.py
5. Variables are preset with defaults and recommended variables are described in full 
    in comments above the call to globalize_physics_vars()
6. To run the sim, run `python Simulator_Main.py` in your terminal. A GUI will pop up showing the aircraft motion. 
7. Enjoy the visual display of lateral stability/instabililty
8. Once satisfied, end the sim by closing the GUI. The sim will end automatically if the aircaft hits one of its failure conditions
9. This generates a file called `data-SIM_START_DATE_AND_TIME.txt` in the folder `./data/`. This file is formatted as:
    ```
    horizontal position (m)     vertical position (m)     bank angle (deg)    time (s)
    ```
10. To plot this data, run `python grapher.py`.
11. The most recent set of data will be plotted
12. To use manual control, run the simulation as normal, and type 'A' or 'D' into the terminal to bank left and right respectively
13. To use the autopilot, run the simulation as normal, and type 'P' into the terminal. Note that manual control is disabled if autopilot is active.
14. The terminal should acknowledge the input and will attempt to stabilize the aircraft
15. In some cases of anhedral, stabilization may be impossible if the autopilot is activated too late.

