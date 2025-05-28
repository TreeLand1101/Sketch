#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from matplotlib.ticker import LogFormatterMathtext, ScalarFormatter

# Default parameters
MEMORY_DEFAULT = 100000
ALPHA_DEFAULT = 0.0001

# Font size constants
TITLE_SIZE = 16
LABEL_SIZE = 14
TICK_SIZE = 12


def plot_rank_frequency(ranks, freqs, out_dir: Path, prefix: str, label_flow: str, log_scale: bool):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ranks, freqs, marker='o', linestyle='-', alpha=0.7)

    flow_cap = label_flow.capitalize()
    if log_scale:
        title_text = f"Rank-Frequency of {flow_cap} Flows (Log Scale)"
        suffix = f"{prefix}_rank-frequency_of_{label_flow}_flows_log.png"
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.xaxis.set_major_formatter(LogFormatterMathtext())
        ax.yaxis.set_major_formatter(LogFormatterMathtext())
    else:
        title_text = f"Rank-Frequency of {flow_cap} Flows"
        suffix = f"{prefix}_rank-frequency_of_{label_flow}_flows.png"
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='y')

    ax.set_title(title_text, fontsize=TITLE_SIZE)
    ax.set_xlabel("Rank", fontsize=LABEL_SIZE)
    ax.set_ylabel("Frequency", fontsize=LABEL_SIZE)
    ax.tick_params(axis='both', labelsize=TICK_SIZE)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    out = out_dir / suffix
    fig.savefig(out)
    plt.close(fig)
    print(f"Saved to {out}")


def plot_cdf(freqs, out_dir: Path, prefix: str, label_flow: str, log_x: bool):
    sorted_freq = np.sort(freqs)
    cdf = np.linspace(1 / freqs.size, 1, freqs.size)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sorted_freq, cdf, marker='o', linestyle='-', alpha=0.7)

    flow_cap = label_flow.capitalize()
    if log_x:
        title_text = f"CDF of {flow_cap} Flows (Log Scale)"
        suffix = f"{prefix}_cdf_of_{label_flow}_flows_log.png"
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(LogFormatterMathtext())
    else:
        title_text = f"CDF of {flow_cap} Flows"
        suffix = f"{prefix}_cdf_of_{label_flow}_flows.png"
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='x')

    ax.set_title(title_text, fontsize=TITLE_SIZE)
    ax.set_xlabel("Frequency", fontsize=LABEL_SIZE)
    ax.set_ylabel("CDF", fontsize=LABEL_SIZE)
    ax.tick_params(axis='both', labelsize=TICK_SIZE)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    out = out_dir / suffix
    fig.savefig(out)
    plt.close(fig)
    print(f"Saved to {out}")


def process_file(out_dir: Path, prefix: str, tag: str, label_flow: str):
    csv_file = out_dir / f"{prefix}_{tag}.csv"
    freqs = np.loadtxt(csv_file, delimiter=',', skiprows=1)
    ranks = np.arange(1, freqs.size + 1)

    plot_rank_frequency(ranks, freqs, out_dir, prefix, label_flow, log_scale=False)
    plot_rank_frequency(ranks, freqs, out_dir, prefix, label_flow, log_scale=True)
    plot_cdf(freqs, out_dir, prefix, label_flow, log_x=False)
    plot_cdf(freqs, out_dir, prefix, label_flow, log_x=True)


def main():
    parser = argparse.ArgumentParser(
        description="Plot Rank-Frequency Distribution and CDF of Flow Frequencies"
    )
    parser.add_argument("stems", nargs='+', help="Dataset stems (folder names)")
    parser.add_argument("--memory", type=int, default=MEMORY_DEFAULT,
                        help="Memory parameter")
    parser.add_argument("--alpha", type=float, default=ALPHA_DEFAULT,
                        help="Alpha threshold")
    args = parser.parse_args()

    prefix = f"memory_{args.memory}_threshold_{args.alpha:.6f}"

    for stem in args.stems:
        out_dir = Path(stem)
        if not out_dir.is_dir():
            print(f"Warning: not a directory: {out_dir}")
            continue

        for tag, label_flow in [("total", "total"), ("retained", "retained")]:
            csv_path = out_dir / f"{prefix}_{tag}.csv"
            if not csv_path.exists():
                print(f"Missing: {csv_path}")
                continue
            print(f"Processing {csv_path.name}...")
            process_file(out_dir, prefix, tag, label_flow)


if __name__ == "__main__":
    main()
