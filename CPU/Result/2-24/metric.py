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
    "memory_100000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.347919, "Query": 0.333422, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400}),
        ("MVSketch(2stage)", {"Insert": 0.280355, "Query": 0.359183, "Recall": 0.542274, "Precision": 0.421132, "F1-score": 0.474087, "AAE": 1336.055556, "ARE": 0.233729}),
        ("StableSketch", {"Insert": 0.301112, "Query": 0.234884, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
        ("StableSketch(2stage)", {"Insert": 0.237258, "Query": 0.279340, "Recall": 0.793003, "Precision": 0.789168, "F1-score": 0.791081, "AAE": 312.789216, "ARE": 0.042036}),
        ("TightSketch", {"Insert": 0.31868, "Query": 0.231021, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
        ("TightSketch(2stage)", {"Insert": 0.245731, "Query": 0.284935, "Recall": 0.927114, "Precision": 0.861789, "F1-score": 0.893258, "AAE": 301.010482, "ARE": 0.048367})
    ],

    "memory_200000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.348649, "Query": 0.340729, "Recall": 0.788144, "Precision": 0.180946, "F1-score": 0.294320, "AAE": 1053.277435, "ARE": 0.218353}),
        ("MVSketch(2stage)", {"Insert": 0.257853, "Query": 0.317110, "Recall": 0.941691, "Precision": 0.818412, "F1-score": 0.875734, "AAE": 224.542828, "ARE": 0.039645}),
        ("StableSketch", {"Insert": 0.280776, "Query": 0.220588, "Recall": 0.769679, "Precision": 1.000000, "F1-score": 0.869852, "AAE": 176.231061, "ARE": 0.015442}),
        ("StableSketch(2stage)", {"Insert": 0.202193, "Query": 0.229141, "Recall": 0.971817, "Precision": 0.882613, "F1-score": 0.925069, "AAE": 169.438000, "ARE": 0.027589}),
        ("TightSketch", {"Insert": 0.303082, "Query": 0.229162, "Recall": 0.984451, "Precision": 1.000000, "F1-score": 0.992165, "AAE": 26.871668, "ARE": 0.005139}),
        ("TightSketch(2stage)", {"Insert": 0.211415, "Query": 0.235395, "Recall": 0.997085, "Precision": 0.876174, "F1-score": 0.932727, "AAE": 173.521442, "ARE": 0.028677})
    ],

    "memory_300000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.351203, "Query": 0.344840, "Recall": 0.916424, "Precision": 0.434162, "F1-score": 0.589191, "AAE": 416.394486, "ARE": 0.087322}),
        ("MVSketch(2stage)", {"Insert": 0.242354, "Query": 0.292015, "Recall": 0.984451, "Precision": 0.920909, "F1-score": 0.951620, "AAE": 127.978282, "ARE": 0.019453}),
        ("StableSketch", {"Insert": 0.274037, "Query": 0.217830, "Recall": 0.808552, "Precision": 1.000000, "F1-score": 0.894143, "AAE": 125.830529, "ARE": 0.016621}),
        ("StableSketch(2stage)", {"Insert": 0.197737, "Query": 0.209395, "Recall": 1.000000, "Precision": 0.923698, "F1-score": 0.960336, "AAE": 123.336249, "ARE": 0.018547}),
        ("TightSketch", {"Insert": 0.29521, "Query": 0.222038, "Recall": 0.991254, "Precision": 1.000000, "F1-score": 0.995608, "AAE": 20.130392, "ARE": 0.003647}),
        ("TightSketch(2stage)", {"Insert": 0.200807, "Query": 0.218096, "Recall": 1.000000, "Precision": 0.923698, "F1-score": 0.960336, "AAE": 123.522838, "ARE": 0.018594})
    ],

    "memory_400000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.354419, "Query": 0.366033, "Recall": 0.973761, "Precision": 0.716738, "F1-score": 0.825711, "AAE": 221.829341, "ARE": 0.045564}),
        ("MVSketch(2stage)", {"Insert": 0.239958, "Query": 0.285740, "Recall": 0.996113, "Precision": 0.943831, "F1-score": 0.969267, "AAE": 93.243902, "ARE": 0.013326}),
        ("StableSketch", {"Insert": 0.267896, "Query": 0.219807, "Recall": 0.849368, "Precision": 1.000000, "F1-score": 0.918550, "AAE": 172.344394, "ARE": 0.019784}),
        ("StableSketch(2stage)", {"Insert": 0.186733, "Query": 0.201119, "Recall": 1.000000, "Precision": 0.944904, "F1-score": 0.971671, "AAE": 92.492711, "ARE": 0.013217}),
        ("TightSketch", {"Insert": 0.292472, "Query": 0.219933, "Recall": 0.992225, "Precision": 1.000000, "F1-score": 0.996098, "AAE": 13.731636, "ARE": 0.002660}),
        ("TightSketch(2stage)", {"Insert": 0.184229, "Query": 0.197652, "Recall": 1.000000, "Precision": 0.944904, "F1-score": 0.971671, "AAE": 92.492711, "ARE": 0.013217})
    ],

    "memory_500000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.354750, "Query": 0.356405, "Recall": 0.994169, "Precision": 0.852500, "F1-score": 0.917900, "AAE": 145.267840, "ARE": 0.028919}),
        ("MVSketch(2stage)", {"Insert": 0.239136, "Query": 0.279251, "Recall": 0.998056, "Precision": 0.952690, "F1-score": 0.974846, "AAE": 71.045764, "ARE": 0.009802}),
        ("StableSketch", {"Insert": 0.268006, "Query": 0.214250, "Recall": 0.846453, "Precision": 1.000000, "F1-score": 0.916842, "AAE": 130.363949, "ARE": 0.015159}),
        ("StableSketch(2stage)", {"Insert": 0.178700, "Query": 0.186007, "Recall": 1.000000, "Precision": 0.953661, "F1-score": 0.976281, "AAE": 71.225462, "ARE": 0.009878}),
        ("TightSketch", {"Insert": 0.284985, "Query": 0.211107, "Recall": 0.992225, "Precision": 1.000000, "F1-score": 0.996098, "AAE": 14.962782, "ARE": 0.002712}),
        ("TightSketch(2stage)", {"Insert": 0.177975, "Query": 0.188826, "Recall": 1.000000, "Precision": 0.953661, "F1-score": 0.976281, "AAE": 71.225462, "ARE": 0.009878})
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