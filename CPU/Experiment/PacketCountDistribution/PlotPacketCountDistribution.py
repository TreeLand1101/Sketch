import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatterMathtext

prefix = "memory_500000_threshold_0.000100"

def plot_rank_frequency_distribution(file_path, title, use_log_scale=False):
    frequencies = np.loadtxt(file_path)
    ranks = np.arange(1, len(frequencies) + 1)
    
    plt.figure(figsize=(10, 5))
    
    if use_log_scale:
        plt.plot(ranks, frequencies, marker='o', linestyle='-', alpha=0.7)
        plt.xscale('log')
        plt.yscale('log')
        
        ax = plt.gca()
        formatter = LogFormatterMathtext()
        ax.xaxis.set_major_formatter(formatter)
        ax.yaxis.set_major_formatter(formatter)
        
        plt.title(f"{title} (Log Scale)")
        plt.xlabel("Rank")
        plt.ylabel("Frequency")
        output_file = file_path.replace('.txt', '') + "_rank_frequency_log.png"
    else:
        plt.plot(ranks, frequencies, marker='o', linestyle='-', alpha=0.7)
        plt.title(f"{title} (Normal Scale)")
        plt.xlabel("Rank")
        plt.ylabel("Frequency")
        output_file = file_path.replace('.txt', '') + "_rank_frequency_normal.png"

    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.savefig(output_file)
    plt.close()
    print(f"saved to {output_file}")

plot_rank_frequency_distribution(prefix + "_all.txt", "Rank-Frequency Distribution for All Flows", use_log_scale=False)
plot_rank_frequency_distribution(prefix + "_all.txt", "Rank-Frequency Distribution for All Flows", use_log_scale=True)

plot_rank_frequency_distribution(prefix + "_filtered.txt", "Rank-Frequency Distribution for Filtered Flows", use_log_scale=False)
plot_rank_frequency_distribution(prefix + "_filtered.txt", "Rank-Frequency Distribution for Filtered Flows", use_log_scale=True)
