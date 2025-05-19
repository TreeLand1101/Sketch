import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def load_data(dataset, memory_values, alpha):
    """
    Load data from CSV files based on dataset, memory values, and alpha
    """
    data = {}
    for memory in memory_values:
        file_path = f"Performance/{dataset}/memory_{memory}_alpha_{alpha}.csv"
        try:
            df = pd.read_csv(file_path)
            data[f"memory_{memory}_alpha_{alpha}"] = [
                (row["Sketch Name"], {
                    "Insert Throughput (Mops)": row["Insert Throughput (Mops)"],
                    "Query Throughput (Mops)": row["Query Throughput (Mops)"],
                    "Recall": row["Recall"],
                    "Precision": row["Precision"],
                    "F1 Score": row["F1 Score"],
                    "AAE": row["AAE"],
                    "ARE": row["ARE"]
                })
                for _, row in df.iterrows()
            ]
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
    return data

def plot_line_chart(data, metric, short_title, alpha, dataset, markers, line_styles,
                    font_size=14, figsize=(10, 6), y_max=None):
    plt.figure(figsize=figsize)
    filtered_data = {k: v for k, v in data.items() if k.endswith(f"alpha_{alpha}")}
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    methods = [entry[0] for entry in filtered_data[memory_keys[0]]] if memory_keys else []
    memories = sorted({int(k.split('_')[1]) // 1000 for k in filtered_data})

    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            key = f"memory_{memory * 1000}_alpha_{alpha}"
            val = next((e[1][metric] for e in filtered_data[key] if e[0] == method), None)
            values.append(val)
        style = line_styles[i % len(line_styles)]
        plt.plot(memories, values,
                 marker=markers[i % len(markers)], linestyle=style,
                 label=method, alpha=0.7, markersize=8)

    plt.xticks(memories, memories, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    plt.ylabel(short_title, fontsize=font_size)
    if y_max is not None:
        plt.ylim(0, y_max)
    elif metric in ["Recall", "Precision", "F1 Score"]:
        plt.ylim(0, 1)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=font_size)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    output_file = f"Performance/{dataset}/{metric}_alpha_{alpha}_line.png"
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved line chart to {output_file}")

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

    plot_line_chart(data, "Insert Throughput (Mops)", "Insert (Mops)", alpha, dataset, markers, line_styles)
    plot_line_chart(data, "Query Throughput (Mops)", "Query (Mops)", alpha, dataset, markers, line_styles)
    plot_line_chart(data, "AAE", "AAE", alpha, dataset, markers, line_styles, y_max=1500)
    plot_line_chart(data, "ARE", "ARE", alpha, dataset, markers, line_styles, y_max=0.3)
    plot_line_chart(data, "Recall", "Recall", alpha, dataset, markers, line_styles)
    plot_line_chart(data, "Precision", "Precision", alpha, dataset, markers, line_styles)
    plot_line_chart(data, "F1 Score", "F1 Score", alpha, dataset, markers, line_styles)