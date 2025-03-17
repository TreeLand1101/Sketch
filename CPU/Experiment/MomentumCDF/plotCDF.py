import matplotlib.pyplot as plt
import numpy as np

def read_log(file_name):
    """
    Reads a log file where each line contains two numbers:
    the first column is the momentum value and the second column is the corresponding CDF value.
    """
    data = np.loadtxt(file_name)
    return data[:, 0], data[:, 1]

mice_file = 'mice_momentum_cdf.log'
elephant_file = 'elephant_momentum_cdf.log'

mice_x, mice_y = read_log(mice_file)
elephant_x, elephant_y = read_log(elephant_file)
plt.plot(mice_x, mice_y, marker='o', linestyle='-', label='Mice Flow')
plt.plot(elephant_x, elephant_y, marker='o', linestyle='-', label='Elephant Flow')

plt.xlabel("Momentum")
plt.ylabel("CDF")
plt.title("Momentum CDF")
plt.legend()
plt.grid(True, which="both", linestyle="--")

plt.savefig("momentum_cdf_plot.png")
