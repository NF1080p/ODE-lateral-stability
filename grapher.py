"""
Functions to graph time series data from simulation flight data. 
"""
import numpy as np
import matplotlib.pyplot as plt
import os

directory_path = "./data/" # Directory that contains data files
files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
files.sort(key=os.path.getmtime)
file_path = files[-1] # Get most recently modified file; most recent simulation data
print(file_path)

def plot_solution(sol_list, t_list, title="a cool title"):
    """
    Plot sol_list vs t_list

    Args:
        sol_list (list): y series 
        t_list (list): t series
        title (str, optional): graph title. Defaults to "a cool title".
    """
    plt.figure()
    plt.plot(t_list, sol_list)
    plt.title(title)
    plt.show(block=False)
    
def plot_solution_from_file(filename=file_path):
    """
    Plot x,y,bank vs t data from a text file

    Args:
        filename (string, optional): text file path. Defaults to file_path.
    """
    # get number of datapoints
    x_list = []
    y_list = []
    bank_list = []
    t_list = []
    
    with open(filename, 'r') as file: # split file int x, y, bank, and t lists
        for line in file:
            values = line.strip().split()
            x_list.append(float(values[0]))
            y_list.append(float(values[1]))
            bank_list.append(float(values[2]))
            t_list.append(float(values[3]))
    plot_solution(x_list, t_list, "x vs t")
    plot_solution(y_list, t_list, "y vs t")
    plot_solution(bank_list, t_list, "bank vs t")
    plt.show()

def plot_solution_more_params(sol_list, t_list, title="a cool title", xlabel="time (s)", ylabel="something cool"):
    """
    Like plot_solution_from_file but with more graph display parameters 

    Args:
        sol_list (list): y series
        t_list (list): t series
        title (str, optional): matplotlib title Defaults to "a cool title".
        xlabel (str, optional): matplotlib x axis label. Defaults to "time (s)".
        ylabel (str, optional): matplotlib y axis label. Defaults to "something cool".
    """
    plt.figure()
    plt.plot(t_list, sol_list)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show(block=False)

if __name__ == "__main__":
    plot_solution_from_file()