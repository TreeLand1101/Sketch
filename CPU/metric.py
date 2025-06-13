#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
import pandas as pd
import sys
import os

LABEL_SIZE  = 20
TICK_SIZE   = 16
LEGEND_SIZE = 16

# Define a vivid colormap
VIVID_CM = colormaps['tab10']  # You can switch to 'tab20' or another for more colors


def load_data(dataset, memory_values, alpha):
    data = {}
    for memory in memory_values:
        file_path = f"Performance/{dataset}/memory_{memory}KB_alpha_{alpha}.csv"
        try:
            df = pd.read_csv(file_path)
            data[f"memory_{memory}KB_alpha_{alpha}"] = [
                (row["Sketch Name"], {
                    "Insert Throughput (Mops)": row["Insert Throughput (Mops)"],
                    "Query Throughput (Mops)": row["Query Throughput (Mops)"],
                    "Recall": row["Recall"],
                    "Precision": row["Precision"],
                    "F1 Score": row["F1 Score"],
                    "AAE": row["AAE"],
                    "ARE": row["ARE"]
                }) for _, row in df.iterrows()
            ]
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
    return data


def write_metric_csv(data, metric, dataset, alpha, memory_values):
    rows = []
    first_key = f"memory_{memory_values[0]}KB_alpha_{alpha}"
    methods = [entry[0] for entry in data.get(first_key, [])]

    for memory in memory_values:
        key = f"memory_{memory}KB_alpha_{alpha}"
        entries = data.get(key, [])
        row = {"memory": f"{memory}KB"}
        for method in methods:
            value = next((e[1][metric] for e in entries if e[0] == method), None)
            row[method] = value
        rows.append(row)

    df_out = pd.DataFrame(rows)
    out_file = f"Performance/{dataset}/{metric.replace(' ', '_')}_alpha_{alpha}.csv"
    df_out.to_csv(out_file, index=False)
    print(f"Saved CSV for {metric} to {out_file}")


def plot_line_chart(data, metric, short_title, alpha, dataset, markers, line_styles,
                    figsize=(12, 8), y_max=None):
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)

    filtered_data = {k: v for k, v in data.items() if k.endswith(f"alpha_{alpha}")}
    memories = sorted(int(k.split('_')[1].rstrip('KB')) for k in filtered_data)
    methods = [e[0] for e in filtered_data[f"memory_{memories[0]}KB_alpha_{alpha}"]]
    x_pos = list(range(len(memories)))

    colors = [VIVID_CM(i % VIVID_CM.N) for i in range(len(methods))]

    for i, method in enumerate(methods):
        values = [
            next((e[1][metric] for e in filtered_data[f"memory_{memory}KB_alpha_{alpha}"] if e[0] == method), None)
            for memory in memories
        ]
        ax.plot(
            x_pos, values,
            marker=markers[i % len(markers)],
            linestyle=line_styles[i % len(line_styles)],
            linewidth=3,                # Thicker lines
            color=colors[i],
            label=method,
            alpha=0.9,
            markersize=8
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels([str(m) for m in memories], fontsize=TICK_SIZE)
    ax.tick_params(axis='y', labelsize=TICK_SIZE)

    ax.set_xlabel("Memory (KB)", fontsize=LABEL_SIZE)
    ax.set_ylabel(short_title, fontsize=LABEL_SIZE)

    if y_max is not None:
        ax.set_ylim(0, y_max)
    elif metric in ["Recall", "Precision", "F1 Score"]:
        ax.set_ylim(0, 1)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=LEGEND_SIZE)
    ax.grid(True, linestyle='--', alpha=0.7)

    output_file = f"Performance/{dataset}/{short_title.replace(' ', '_')}_alpha_{alpha}_line.png"
    fig.savefig(output_file, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved line chart to {output_file}")


def plot_bar_chart(data, metric, short_title, alpha, dataset,
                   figsize=(12, 8), y_max=None):
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)

    filtered_data = {k: v for k, v in data.items() if k.endswith(f"alpha_{alpha}")}
    memories = sorted(int(k.split('_')[1].rstrip('KB')) for k in filtered_data)
    methods = [e[0] for e in filtered_data[f"memory_{memories[0]}KB_alpha_{alpha}"]]
    num_methods = len(methods)
    x = np.arange(len(memories))
    width = 0.8 / num_methods

    for i, method in enumerate(methods):
        values = [
            next((e[1][metric] for e in filtered_data[f"memory_{memory}KB_alpha_{alpha}"] if e[0] == method), None)
            for memory in memories
        ]
        ax.bar(
            x + i*width, values, width=width,
            color=VIVID_CM(i % VIVID_CM.N),
            label=method  # Added label for legend
        )

    ax.set_xticks(x + width*(num_methods-1)/2)
    ax.set_xticklabels([str(m) for m in memories], fontsize=TICK_SIZE)
    ax.tick_params(axis='y', labelsize=TICK_SIZE)

    ax.set_xlabel("Memory (KB)", fontsize=LABEL_SIZE)
    ax.set_ylabel(short_title, fontsize=LABEL_SIZE)

    if y_max is not None:
        ax.set_ylim(0, y_max)
    elif metric in ["Recall", "Precision", "F1 Score"]:
        ax.set_ylim(0, 1)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=LEGEND_SIZE)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    output_file = f"Performance/{dataset}/{short_title}_alpha_{alpha}_bar.png"
    fig.savefig(output_file, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved bar chart to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python metric.py <dataset> <alpha> <memory1> <memory2> ...")
        sys.exit(1)
    dataset = sys.argv[1]
    alpha = float(sys.argv[2])
    memory_values = list(map(int, sys.argv[3:]))

    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
    line_styles = ['-', '--']

    data = load_data(dataset, memory_values, alpha)

    if not data:
        print("No valid data loaded.")
        sys.exit(1)

    # Line charts
    # plot_line_chart(data, "Insert Throughput (Mops)", "Insert Throughput (Mops)", alpha, dataset, markers, line_styles)
    # plot_line_chart(data, "Query Throughput (Mops)", "Query Throughput (Mops)", alpha, dataset, markers, line_styles)
    # plot_line_chart(data, "AAE", "AAE", alpha, dataset, markers, line_styles, y_max=1500)
    # plot_line_chart(data, "ARE", "ARE", alpha, dataset, markers, line_styles, y_max=0.3)
    # plot_line_chart(data, "Recall", "Recall", alpha, dataset, markers, line_styles)
    # plot_line_chart(data, "Precision", "Precision", alpha, dataset, markers, line_styles)
    # plot_line_chart(data, "F1 Score", "F1 Score", alpha, dataset, markers, line_styles)

    # Bar charts
    plot_bar_chart(data, "Insert Throughput (Mops)", "Insert Throughput (Mops)", alpha, dataset)
    plot_bar_chart(data, "Query Throughput (Mops)", "Query Throughput (Mops)", alpha, dataset)

    # CSV outputs
    metrics = ["Insert Throughput (Mops)", "Query Throughput (Mops)", "Recall", "Precision", "F1 Score", "AAE", "ARE"]
    for metric in metrics:
        write_metric_csv(data, metric, dataset, alpha, memory_values)
