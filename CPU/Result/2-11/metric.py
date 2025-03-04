import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_bar_chart(data, metric, short_title, threshold, hatch_patterns, font_size=14):
    """Plot bar chart (fixed threshold, comparing different memory and sketch methods)
       and print the overall average value for each method."""
    plt.figure(figsize=(10, 6))
    
    # Filter data by threshold
    filtered_data = { key: val for key, val in data.items() if key.endswith(f"threshold_{threshold:.4f}") }
    
    # Use the order from the first memory key's list to determine method order
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    if memory_keys:
        methods = [ entry[0] for entry in filtered_data[memory_keys[0]] ]
    else:
        methods = []
    
    # Get memory values (in KB) sorted by memory size
    memories = sorted({ int(key.split('_')[1]) // 1000 for key in filtered_data.keys() })
    
    width = 0.2  # Control bar spacing
    x = np.arange(len(memories))  # X-axis positions
    
    # Plot bars for each method in the given order, averaging values if multiple exist
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}_threshold_{threshold:.4f}"
            # Collect all metric values for the current method at this memory
            method_values = [entry[1][metric] for entry in filtered_data[memory_key] if entry[0] == method]
            if method_values:
                avg_value = sum(method_values) / len(method_values)
            else:
                avg_value = None
            values.append(avg_value)
        # 計算所有 memory 的平均值
        overall_avg = np.mean([v for v in values if v is not None])
        if metric in ["Insert", "Query"]:
            print(f"{method}: {short_title} average = {overall_avg:.3f} ms")
        else:
            print(f"{method}: {short_title} average = {overall_avg:.3f}")
            
        bars = plt.bar(x + i * width, values, width, label=method, hatch=hatch_patterns[i % len(hatch_patterns)])
        for bar in bars:
            bar.set_edgecolor('black')  # Add border for better contrast
    
    # Set x and y ticks with specified font size, and x-axis labels not rotated
    plt.xticks(x + width * (len(methods) - 1) / 2, memories, rotation=0, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    if metric in ["Insert", "Query"]:
        plt.ylabel(f"{short_title} (ms)", fontsize=font_size)
    else:
        plt.ylabel(short_title, fontsize=font_size)
    plt.legend(loc='upper right', fontsize=font_size)  # Fixed legend position
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{metric}_{threshold:.4f}.png')
    plt.close()

def plot_line_chart(data, metric, short_title, threshold, markers, font_size=14):
    """Plot line chart (fixed threshold, comparing different memory and sketch methods)"""
    plt.figure(figsize=(10, 6))
    
    # Filter data by threshold
    filtered_data = { key: val for key, val in data.items() if key.endswith(f"threshold_{threshold:.4f}") }
    
    # Use the order from the first memory key's list to determine method order
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    if memory_keys:
        methods = [ entry[0] for entry in filtered_data[memory_keys[0]] ]
    else:
        methods = []
    
    # Get memory values (in KB)
    memories = sorted({ int(key.split('_')[1]) // 1000 for key in filtered_data.keys() })
    
    # Plot line for each method in the given order
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}_threshold_{threshold:.4f}"
            method_value = next((entry[1][metric] for entry in filtered_data[memory_key] if entry[0] == method), None)
            values.append(method_value)
        plt.plot(memories, values, marker=markers[i % len(markers)], linestyle='-', label=method)
    
    # Set x and y ticks with specified font size
    plt.xticks(memories, memories, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    plt.ylabel(short_title, fontsize=font_size)
    if metric in ["Recall", "Precision", "F1-score"]:
        plt.ylim(0, 1)
    plt.legend(loc='upper right', fontsize=font_size)  # Fixed legend position
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f'{metric}_{threshold:.4f}.png')
    plt.close()

# ---------------------------
# Test data (Data structure changed to List)
data = {
    "memory_100000_threshold_0.0001": [
        ("OurSketch", {"Insert": 0.143302, "Query": 0.117792, "Recall": 0.900875, "Precision": 0.743384, "F1-score": 0.814587, "AAE": 200.249191, "ARE": 0.035055}),
        ("Elastic", {"Insert": 0.171799, "Query": 0.152786, "Recall": 0.736638, "Precision": 0.807242, "F1-score": 0.770325, "AAE": 1094.941953, "ARE": 0.161874}),
        ("CocoSketch", {"Insert": 0.164452, "Query": 0.138738, "Recall": 0.852284, "Precision": 0.149378, "F1-score": 0.254203, "AAE": 987.581528, "ARE": 0.198778}),
        ("StableSketch", {"Insert": 0.304445, "Query": 0.229796, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543})
    ],
    "memory_200000_threshold_0.0001": [
        ("OurSketch", {"Insert": 0.145913, "Query": 0.112879, "Recall": 0.959184, "Precision": 0.950867, "F1-score": 0.955007, "AAE": 77.605876, "ARE": 0.012953}),
        ("Elastic", {"Insert": 0.173143, "Query": 0.160862, "Recall": 0.935860, "Precision": 0.799834, "F1-score": 0.862517, "AAE": 422.763240, "ARE": 0.073914}),
        ("CocoSketch", {"Insert": 0.159396, "Query": 0.133753, "Recall": 0.953353, "Precision": 0.692308, "F1-score": 0.802126, "AAE": 304.227319, "ARE": 0.040000}),
        ("StableSketch", {"Insert": 0.283417, "Query": 0.225754, "Recall": 0.769679, "Precision": 1.000000, "F1-score": 0.869852, "AAE": 176.231061, "ARE": 0.015442})
    ],
    "memory_300000_threshold_0.0001": [
        ("OurSketch", {"Insert": 0.140763, "Query": 0.111026, "Recall": 0.976676, "Precision": 0.994065, "F1-score": 0.985294, "AAE": 46.131343, "ARE": 0.007383}),
        ("Elastic", {"Insert": 0.174031, "Query": 0.160608, "Recall": 0.986395, "Precision": 0.856540, "F1-score": 0.916893, "AAE": 242.234483, "ARE": 0.044576}),
        ("CocoSketch", {"Insert": 0.160962, "Query": 0.136067, "Recall": 0.967930, "Precision": 0.857143, "F1-score": 0.909174, "AAE": 163.956827, "ARE": 0.031338}),
        ("StableSketch", {"Insert": 0.28954, "Query": 0.233696, "Recall": 0.808552, "Precision": 1.000000, "F1-score": 0.894143, "AAE": 125.830529, "ARE": 0.016621})
    ],
    "memory_400000_threshold_0.0001": [
        ("OurSketch", {"Insert": 0.13544, "Query": 0.112978, "Recall": 0.983479, "Precision": 0.996063, "F1-score": 0.989731, "AAE": 37.168972, "ARE": 0.006553}),
        ("Elastic", {"Insert": 0.169176, "Query": 0.156225, "Recall": 0.986395, "Precision": 0.905442, "F1-score": 0.944186, "AAE": 155.718227, "ARE": 0.028209}),
        ("CocoSketch", {"Insert": 0.154831, "Query": 0.136938, "Recall": 0.976676, "Precision": 0.924563, "F1-score": 0.949905, "AAE": 98.410945, "ARE": 0.018744}),
        ("StableSketch", {"Insert": 0.276372, "Query": 0.2211, "Recall": 0.849368, "Precision": 1.000000, "F1-score": 0.918550, "AAE": 172.344394, "ARE": 0.019784})
    ],
    "memory_500000_threshold_0.0001": [
        ("OurSketch", {"Insert": 0.141334, "Query": 0.115641, "Recall": 0.990282, "Precision": 0.998041, "F1-score": 0.994146, "AAE": 28.037291, "ARE": 0.004578}),
        ("Elastic", {"Insert": 0.178444, "Query": 0.154073, "Recall": 0.991254, "Precision": 0.919748, "F1-score": 0.954163, "AAE": 114.371569, "ARE": 0.021139}),
        ("CocoSketch", {"Insert": 0.160239, "Query": 0.143605, "Recall": 0.979592, "Precision": 0.936803, "F1-score": 0.957720, "AAE": 84.376984, "ARE": 0.015874}),
        ("StableSketch", {"Insert": 0.274671, "Query": 0.223546, "Recall": 0.846453, "Precision": 1.000000, "F1-score": 0.916842, "AAE": 130.363949, "ARE": 0.015159})
    ],
}

# Plot bar charts (fixed threshold, comparing different memory)
thresholds = [0.0001]
markers = ['o', 's', '^', 'D', 'v']  # Different markers for methods
hatch_patterns = ['/', '\\', '|', '-', '+']  # Different bar patterns

for threshold in thresholds:
    plot_bar_chart(data, "Insert", "Insert", threshold, hatch_patterns, font_size=14)
    plot_bar_chart(data, "Query", "Query", threshold, hatch_patterns, font_size=14)
    
    # Plot line charts
    plot_line_chart(data, "AAE", "AAE", threshold, markers, font_size=14)
    plot_line_chart(data, "ARE", "ARE", threshold, markers, font_size=14)
    plot_line_chart(data, "Recall", "Recall", threshold, markers, font_size=14)
    plot_line_chart(data, "Precision", "Precision", threshold, markers, font_size=14)
    plot_line_chart(data, "F1-score", "F1-score", threshold, markers, font_size=14)
