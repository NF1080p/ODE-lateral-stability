import numpy as np
import matplotlib.pyplot as plt
import os

directory_path = "./data/" # directory that contains data files
files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
files.sort(key=os.path.getmtime)
file_path = files[-1]
print(file_path)

def plot_solution(sol_list, t_list, title="a cool title"):
    plt.figure()
    plt.plot(t_list, sol_list)
    plt.title(title)
    plt.show(block=False)
    
def plot_solution_from_file(filename=file_path):
    # get number of datapoints
    x_list = []
    y_list = []
    bank_list = []
    t_list = []
    with open(filename, 'r') as file:
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

if __name__ == "__main__":
    print("fello world")
    plot_solution_from_file()