#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from matplotlib.ticker import LogFormatterMathtext, ScalarFormatter

MEMORY_DEFAULT = 100000
ALPHA_DEFAULT = 0.0001

def plot_rank_frequency(ranks, freqs, out_dir: Path, prefix: str, tag: str, label: str, log_scale: bool):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ranks, freqs, marker='o', linestyle='-', alpha=0.7)

    if log_scale:
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.xaxis.set_major_formatter(LogFormatterMathtext())
        ax.yaxis.set_major_formatter(LogFormatterMathtext())
        ax.set_title(f"{label} Rank-Frequency Distribution (Log Scale)")
        suffix = f"{prefix}_{tag}_rank_frequency_log.png"
    else:
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='y')
        ax.set_title(f"{label} Rank-Frequency Distribution")
        suffix = f"{prefix}_{tag}_rank_frequency.png"

    ax.set_xlabel("Rank")
    ax.set_ylabel("Frequency")
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)

    out = out_dir / suffix
    fig.savefig(out)
    plt.close(fig)
    print(f"saved to {out}")


def plot_cdf(freqs, out_dir: Path, prefix: str, tag: str, label: str, log_x: bool):
    sorted_freq = np.sort(freqs)
    cdf = np.linspace(1 / freqs.size, 1, freqs.size)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sorted_freq, cdf, marker='o', linestyle='-', alpha=0.7)

    if log_x:
        ax.set_xscale('log')
        ax.xaxis.set_major_formatter(LogFormatterMathtext())
        ax.set_title(f"{label} Frequency CDF (Log Scale)")
        suffix = f"{prefix}_{tag}_frequency_cdf_log.png"
    else:
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.ticklabel_format(style='plain', axis='x')
        ax.set_title(f"{label} Frequency CDF")
        suffix = f"{prefix}_{tag}_frequency_cdf.png"

    ax.set_xlabel("Frequency")
    ax.set_ylabel("Probability")
    ax.grid(True, which="both", linestyle='--', linewidth=0.5)

    out = out_dir / suffix
    fig.savefig(out)
    plt.close(fig)
    print(f"saved to {out}")


def process_file(out_dir: Path, prefix: str, tag: str, label: str):
    txt_file = out_dir / f"{prefix}_{tag}.txt"
    freqs = np.loadtxt(txt_file)
    ranks = np.arange(1, freqs.size + 1)

    plot_rank_frequency(ranks, freqs, out_dir, prefix, tag, label, log_scale=False)
    plot_rank_frequency(ranks, freqs, out_dir, prefix, tag, label, log_scale=True)

    plot_cdf(freqs, out_dir, prefix, tag, label, log_x=False)
    plot_cdf(freqs, out_dir, prefix, tag, label, log_x=True)


def main():
    parser = argparse.ArgumentParser(
        description="Plot rank-frequency and CDF from frequency files"
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

        for tag, label in [("all", "All Flows"), ("filtered", "Filtered Flows")]:
            txt_path = out_dir / f"{prefix}_{tag}.txt"
            if not txt_path.exists():
                print(f"Missing: {txt_path}")
                continue
            print(f"Processing {txt_path.name}...")
            process_file(out_dir, prefix, tag, label)

if __name__ == "__main__":
    main()