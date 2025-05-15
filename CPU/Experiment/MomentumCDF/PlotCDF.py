import matplotlib.pyplot as plt
import numpy as np

def read_csv(file_name):
    """
    Reads a CSV file with header 'momentum,cdf'
    and returns two arrays: momentum values and CDF values.
    """
    data = np.loadtxt(file_name, delimiter=',', skiprows=1)
    return data[:, 0], data[:, 1]

# File names
nonheavy_file = 'nonheavy_momentum_cdf.csv'
heavyhitter_file = 'heavyhitter_momentum_cdf.csv'

# Read data
nonheavy_x, nonheavy_y = read_csv(nonheavy_file)
heavyhitter_x, heavyhitter_y = read_csv(heavyhitter_file)

# Plot the data
plt.plot(nonheavy_x, nonheavy_y, marker='o', linestyle='-', label='Non-Heavy Flows')
plt.plot(heavyhitter_x, heavyhitter_y, marker='o', linestyle='-', label='Heavy Hitters')

# Set labels and title
plt.xlabel("Momentum")
plt.ylabel("CDF")
plt.title("Momentum CDF for Non-Heavy Flows and Heavy-Hitter")
plt.legend()
plt.grid(True, which="both", linestyle="--")

# Save the plot
plt.savefig("momentum_cdf_plot.png")
