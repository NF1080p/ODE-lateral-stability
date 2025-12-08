# ODE-lateral-stability

This repo contains code for our MAT292 Final Project. We created a simulation to help analyze lateral stability in an aircraft. 

(copy paste shortened version of our intro here)



## Installation

Our code is written in Python3. To reproduce our results, start by installing the dependencies.

1. Clone this repository
2. Create and activate virtual environment in Python
3. Install the dependendencies: `pip install pyglet numpy pynput matplotlib sympy`

Alternative (No virtual environment)

1. Clone this repository
2. Ensure python 3, math, matplotlib, numpy, os, pynput, sympy, and pyglet are installed via 'pip install' commands
3. 

To run the sim, run `python vis.py` in your terminal. A GUI will pop up showing the aircraft motion. Close the sim by closing the GUI. This generates a file called `data-SIM_START_DATE_AND_TIME.txt` in the folder `./data/`. This file is formatted as:

```
horizontal position (m)     vertical position (m)     bank angle (deg)    time (s)
```

To plot this data, run `python grapher.py`.  

