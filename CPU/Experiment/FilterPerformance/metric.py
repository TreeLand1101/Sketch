import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

def load_data(memory_values):
    """Load data from CSV files, matching the original dictionary format"""
    data = {}
    for memory in memory_values:
        file_path = f"memory_{memory}.csv"
        try:
            df = pd.read_csv(file_path)
            data[f"memory_{memory}"] = [
                (row["Filter Name"], {
                    "Insert": row["Insert Throughput (Mops/s)"],
                    "Query": row["Query Throughput (Mops/s)"],
                    "AAE": row["AAE"],
                    "ARE": row["ARE"]
                }) for _, row in df.iterrows()
            ]
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
    return data

def plot_line_chart(data, metric, short_title, markers, line_styles, trace_label="", font_size=14, figsize=(10, 6)):
    """Plot a line chart for throughput (Insert and Query) and error metrics (AAE and ARE)"""
    plt.figure(figsize=figsize)
    
    memory_keys = sorted(data.keys(), key=lambda k: int(k.split('_')[1]))
    methods = [entry[0] for entry in data[memory_keys[0]]]
    memories = sorted({int(key.split('_')[1]) // 1000 for key in memory_keys})
    
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}"
            method_value = next((entry[1][metric] for entry in data[memory_key] if entry[0] == method), None)
            values.append(method_value)
        
        style_index = i % len(line_styles)
        plt.plot(memories, values,
                 marker=markers[i % len(markers)],
                 linestyle=line_styles[style_index],
                 label=method,
                 alpha=0.7,
                 markersize=8)
    
    plt.xticks(memories, memories, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    plt.ylabel(short_title, fontsize=font_size)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=font_size)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_file = f'{trace_label}_{metric}_line.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved line chart to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python metric.py <memory_value1> <memory_value2> ...")
        sys.exit(1)
    
    memory_values = sys.argv[1:]
    data = load_data(memory_values)
    
    if not data:
        print("No data found. Please check if CSV files are generated correctly.")
        sys.exit(1)
    
    trace_label = "FilterPerformance"
    markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
    line_styles = ['-', '--']
    
    plot_line_chart(data, "Insert", "Insert Throughput (Mops/s)", markers, line_styles, trace_label=trace_label)
    plot_line_chart(data, "Query", "Query Throughput (Mops/s)", markers, line_styles, trace_label=trace_label)
    plot_line_chart(data, "AAE", "AAE", markers, line_styles, trace_label=trace_label)
    plot_line_chart(data, "ARE", "ARE", markers, line_styles, trace_label=trace_label)