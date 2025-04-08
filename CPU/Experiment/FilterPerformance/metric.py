import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_bar_chart(data, metric, short_title, hatch_patterns, trace_label="", font_size=14, figsize=(10, 6)):
    """
    Plot a bar chart comparing different memory sizes for various sketch methods.
    
    Parameters:
        data: dict, keys are in the format "memory_xxxxx"
        metric: str, the metric to plot (e.g., "Insert" or "Query")
        short_title: str, title for the y-axis label
        hatch_patterns: list of str, patterns to use for bar hatching
        trace_label: str, an optional label for the trace (used in printed messages and output filename)
        font_size: int, font size for labels
        figsize: tuple, figure size
    """
    plt.figure(figsize=figsize)
    
    # Sort keys by memory size, e.g., "memory_50000", "memory_100000", etc.
    memory_keys = sorted(data.keys(), key=lambda k: int(k.split('_')[1]))
    # Get the list of methods from the first memory entry
    methods = [entry[0] for entry in data[memory_keys[0]]]
    
    # Extract memory sizes in KB
    memories = sorted({int(key.split('_')[1]) // 1000 for key in memory_keys})
    
    width = 0.15  
    x = np.arange(len(memories)) * 1.5 

    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}"
            # Get the metric values for the given method
            method_values = [entry[1][metric] for entry in data[memory_key] if entry[0] == method]
            avg_value = sum(method_values) / len(method_values) if method_values else None
            values.append(avg_value)
        
        overall_avg = np.mean([v for v in values if v is not None])
        print(f"{trace_label} - {method}: {short_title} average = {overall_avg:.3f}")
        
        bars = plt.bar(x - (len(methods) - 1) * width / 2 + i * width, values, width,
                       label=method, hatch=hatch_patterns[i % len(hatch_patterns)])
        for bar in bars:
            bar.set_edgecolor('black')
    
    plt.xticks(x, memories, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    # If metric is time-based, add unit "ms"
    plt.ylabel(f"{short_title} (ms)", fontsize=font_size)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, fontsize=font_size)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    output_file = f'{trace_label}_{metric}_bar.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved bar chart to {output_file}")

def plot_line_chart(data, metric, short_title, markers, line_styles, trace_label="", font_size=14, figsize=(10, 6)):
    """
    Plot a line chart comparing different memory sizes for various sketch methods.
    
    Parameters:
        data: dict, keys are in the format "memory_xxxxx"
        metric: str, the metric to plot (e.g., "AAE", "ARE")
        short_title: str, title for the y-axis label
        markers: list of str, marker styles for plotting
        line_styles: list of str, line styles for plotting
        trace_label: str, an optional label for the trace (used in printed messages and output filename)
        font_size: int, font size for labels
        figsize: tuple, figure size
    """
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

# ----- Example Data ----- #
# CAIDA2016 example data with keys in the format "memory_xxxxx"
CAIDA2016 = {
    "memory_25000": [
        ("CUCBF", {"Insert": 0.048493, "Query": 0.04324, "AAE": 2101.9, "ARE": 964.61}),
        ("CMSketch (d = 4)", {"Insert": 0.0881667, "Query": 0.0842106, "AAE": 5531.77, "ARE": 2525.17}),
        ("CMSketch (d = 2)", {"Insert": 0.0465235, "Query": 0.0422373, "AAE": 3075.34, "ARE": 1403.35}),
        ("CUSketch (d = 4)", {"Insert": 0.0911642, "Query": 0.0831371, "AAE": 3013, "ARE": 1383.41}),
        ("CUSketch (d = 2)", {"Insert": 0.0474355, "Query": 0.04238, "AAE": 2106.68, "ARE": 966.505}),
    ],
    "memory_50000": [
        ("CUCBF", {"Insert": 0.0486111, "Query": 0.044212, "AAE": 920.945, "ARE": 424.311}),
        ("CMSketch (d = 4)", {"Insert": 0.0900734, "Query": 0.0838306, "AAE": 2333.08, "ARE": 1064.67}),
        ("CMSketch (d = 2)", {"Insert": 0.0469074, "Query": 0.0441466, "AAE": 1330.5, "ARE": 607.137}),
        ("CUSketch (d = 4)", {"Insert": 0.0932119, "Query": 0.0831253, "AAE": 1289, "ARE": 594.799}),
        ("CUSketch (d = 2)", {"Insert": 0.0477625, "Query": 0.0431878, "AAE": 923.238, "ARE": 425.567}),
    ],
    "memory_75000": [
        ("CUCBF", {"Insert": 0.0491939, "Query": 0.0436499, "AAE": 563.311, "ARE": 260.683}),
        ("CMSketch (d = 4)", {"Insert": 0.0912972, "Query": 0.0832254, "AAE": 1387.17, "ARE": 632.996}),
        ("CMSketch (d = 2)", {"Insert": 0.0466963, "Query": 0.0428217, "AAE": 806.731, "ARE": 367.82}),
        ("CUSketch (d = 4)", {"Insert": 0.0927431, "Query": 0.0839826, "AAE": 768.718, "ARE": 356.484}),
        ("CUSketch (d = 2)", {"Insert": 0.0481841, "Query": 0.0436529, "AAE": 562.575, "ARE": 260.111}),
    ],
    "memory_100000": [
        ("CUCBF", {"Insert": 0.0496697, "Query": 0.046035, "AAE": 393.697, "ARE": 182.761}),
        ("CMSketch (d = 4)", {"Insert": 0.0941356, "Query": 0.0882141, "AAE": 953.778, "ARE": 434.912}),
        ("CMSketch (d = 2)", {"Insert": 0.0498252, "Query": 0.0450795, "AAE": 562.123, "ARE": 256.181}),
        ("CUSketch (d = 4)", {"Insert": 0.0963442, "Query": 0.0866493, "AAE": 530.908, "ARE": 247.304}),
        ("CUSketch (d = 2)", {"Insert": 0.0494834, "Query": 0.045605, "AAE": 393.417, "ARE": 182.599}),
    ]
}

# If data for CAIDA2018 and CAIDA2019 exist, they should follow the same format.
CAIDA2018 = {}  # Placeholder if available
CAIDA2019 = {}  # Placeholder if available

all_data_traces = [
    ("CAIDA2016", CAIDA2016),
    # ("CAIDA2018", CAIDA2018),
    # ("CAIDA2019", CAIDA2019)
]

# Pre-defined markers, hatch patterns, and line styles
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
line_styles = ['-', '--']

# Generate charts for each trace
for trace_label, data in all_data_traces:
    # Plot bar charts for "Insert" and "Query" metrics
    plot_bar_chart(data, "Insert", "Insert", hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_bar_chart(data, "Query", "Query", hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))
    
    # Plot line charts for error metrics "AAE" and "ARE"
    plot_line_chart(data, "AAE", "AAE", markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "ARE", "ARE", markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
