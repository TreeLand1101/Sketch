import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
def plot_bar_chart(data, metric, short_title, threshold, hatch_patterns, font_size=14, figsize=(10, 6)):
    """Plot bar chart (fixed threshold, comparing different memory and sketch methods)
       and print the overall average value for each method."""
    plt.figure(figsize=figsize)  
    
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
    
    width = 0.15  
    x = np.arange(len(memories)) * 1.5  # 定义X轴刻度
    
    # Plot bars for each method in the given order, averaging values if multiple exist
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}_threshold_{threshold:.4f}"
            method_values = [entry[1][metric] for entry in filtered_data[memory_key] if entry[0] == method]
            avg_value = sum(method_values) / len(method_values) if method_values else None
            values.append(avg_value)
        
        overall_avg = np.mean([v for v in values if v is not None])
        if metric in ["Insert", "Query"]:
            print(f"{method}: {short_title} average = {overall_avg:.3f} ms")
        else:
            print(f"{method}: {short_title} average = {overall_avg:.3f}")
        
        # 让 bars 居中对齐 xticks
        bars = plt.bar(x - (len(methods) - 1) * width / 2 + i * width, values, width, 
                       label=method, hatch=hatch_patterns[i % len(hatch_patterns)])
        for bar in bars:
            bar.set_edgecolor('black')
    
    plt.xticks(x, memories, rotation=0, fontsize=font_size) 
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    if metric in ["Insert", "Query"]:
        plt.ylabel(f"{short_title} (ms)", fontsize=font_size)
    else:
        plt.ylabel(short_title, fontsize=font_size)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, fontsize=font_size) 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{metric}_{threshold:.4f}.png', bbox_inches='tight')
    plt.close()


def plot_line_chart(data, metric, short_title, threshold, markers, line_styles, font_size=14, figsize=(10, 6)):
    """Plot line chart (fixed threshold, comparing different memory and sketch methods)"""
    plt.figure(figsize=figsize)
    
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
    if metric in ["Recall", "Precision", "F1-score"]:
        plt.ylim(0, 1)
    
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=font_size)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(f'{metric}_{threshold:.4f}.png', bbox_inches='tight')
    plt.close()

# ---------------------------
# Test data (Data structure changed to List)
data = {
    "memory_50000_threshold_0.0001": [
        ("MomentumSketch_SIMD", {"Insert": 0.0932406, "Query": 0.0631119, "Recall": 0.789116, "Precision": 1.000000, "F1-score": 0.882129, "AAE": 213.748768, "ARE": 0.036388}),
        ("MomentumSketch", {"Insert": 0.135775, "Query": 0.111545, "Recall": 0.790087, "Precision": 1.000000, "F1-score": 0.882736, "AAE": 231.557196, "ARE": 0.038627})
    ],

    "memory_100000_threshold_0.0001": [
        ("MomentumSketch_SIMD", {"Insert": 0.0907377, "Query": 0.0631165, "Recall": 0.943635, "Precision": 1.000000, "F1-score": 0.971000, "AAE": 65.814624, "ARE": 0.011863}),
        ("MomentumSketch", {"Insert": 0.133761, "Query": 0.111430, "Recall": 0.944606, "Precision": 1.000000, "F1-score": 0.971514, "AAE": 71.083333, "ARE": 0.012484})
    ],

    "memory_150000_threshold_0.0001": [
        ("MomentumSketch_SIMD", {"Insert": 0.0892665, "Query": 0.0638704, "Recall": 0.972789, "Precision": 1.000000, "F1-score": 0.986207, "AAE": 36.616384, "ARE": 0.006568}),
        ("MomentumSketch", {"Insert": 0.131281, "Query": 0.112646, "Recall": 0.975705, "Precision": 1.000000, "F1-score": 0.987703, "AAE": 33.272908, "ARE": 0.005889})
    ],

    "memory_200000_threshold_0.0001": [
        ("MomentumSketch_SIMD", {"Insert": 0.0882055, "Query": 0.0647664, "Recall": 0.984451, "Precision": 1.000000, "F1-score": 0.992165, "AAE": 23.022705, "ARE": 0.004211}),
        ("MomentumSketch", {"Insert": 0.134893, "Query": 0.113648, "Recall": 0.986395, "Precision": 1.000000, "F1-score": 0.993151, "AAE": 30.192118, "ARE": 0.004964})
    ],

    "memory_250000_threshold_0.0001": [
        ("MomentumSketch_SIMD", {"Insert": 0.0874944, "Query": 0.0651839, "Recall": 0.992225, "Precision": 1.000000, "F1-score": 0.996098, "AAE": 21.448580, "ARE": 0.003762}),
        ("MomentumSketch", {"Insert": 0.128921, "Query": 0.106048, "Recall": 0.993197, "Precision": 1.000000, "F1-score": 0.996587, "AAE": 23.285714, "ARE": 0.004019})
    ]
}

# Plot bar charts and line charts (fixed threshold, comparing different memory)
thresholds = [0.0001]
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
line_styles = ['-', '--']

for threshold in thresholds:
    plot_bar_chart(data, "Insert", "Insert", threshold, hatch_patterns, font_size=14, figsize=(10, 6))
    plot_bar_chart(data, "Query", "Query", threshold, hatch_patterns, font_size=14, figsize=(10, 6))
    
    # Plot line charts with line styles
    plot_line_chart(data, "AAE", "AAE", threshold, markers, line_styles, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "ARE", "ARE", threshold, markers, line_styles, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Recall", "Recall", threshold, markers, line_styles, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Precision", "Precision", threshold, markers, line_styles, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "F1-score", "F1-score", threshold, markers, line_styles, font_size=14, figsize=(10, 6))