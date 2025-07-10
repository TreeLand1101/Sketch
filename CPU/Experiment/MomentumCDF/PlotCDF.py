import matplotlib.pyplot as plt
import numpy as np
import os
import sys

LABEL_SIZE  = 20
TICK_SIZE   = 14
LEGEND_SIZE = 14

def read_csv(file_name):
    data = np.loadtxt(file_name, delimiter=',', skiprows=1)
    return data[:, 0], data[:, 1]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 PlotCDF.py <dataset1> [dataset2 ...]")
        sys.exit(1)

    datasets = sys.argv[1:]
    CAP_VALUE = 10**9
    
    for ds in datasets:
        folder = ds

        nonheavy_file    = os.path.join(folder, "nonheavy_momentum_cdf.csv")
        heavyhitter_file = os.path.join(folder, "heavyhitter_momentum_cdf.csv")

        if not os.path.exists(nonheavy_file) or not os.path.exists(heavyhitter_file):
            print(f"Warning: CSV not found in folder '{folder}'. Skipping.")
            continue

        nonheavy_x, nonheavy_y = read_csv(nonheavy_file)
        heavy_x,    heavy_y    = read_csv(heavyhitter_file)

        nonheavy_x = np.minimum(nonheavy_x, CAP_VALUE)
        heavy_x    = np.minimum(heavy_x, CAP_VALUE)

        plt.figure(figsize=(8, 5))

        plt.plot(nonheavy_x, nonheavy_y,
                 marker='o', linestyle='-',
                 label='Non-Heavy Flows')
        plt.plot(heavy_x,    heavy_y,
                 marker='o', linestyle='-',
                 label='Heavy Hitters')

        plt.xlabel("Momentum", fontsize=LABEL_SIZE)
        plt.ylabel("CDF",      fontsize=LABEL_SIZE)

        plt.xticks(fontsize=TICK_SIZE)
        plt.yticks(fontsize=TICK_SIZE)

        plt.legend(fontsize=LEGEND_SIZE)

        plt.grid(True, which="both", linestyle="--", alpha=0.7)

        out_png = os.path.join(folder, "momentum_cdf_plot.png")
        plt.tight_layout()
        plt.savefig(out_png, bbox_inches='tight')
        plt.close()

        print(f"Saved plot: {out_png}")
