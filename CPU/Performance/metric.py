import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_bar_chart(data, metric, short_title, threshold, hatch_patterns, trace_label="", font_size=14, figsize=(10, 6)):
    """Plot bar chart (fixed threshold, comparing different memory and sketch methods)
       and print the overall average value for each method."""
    plt.figure(figsize=figsize)  
    
    filtered_data = { key: val for key, val in data.items() if key.endswith(f"threshold_{threshold:.4f}") }
    
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    if memory_keys:
        methods = [ entry[0] for entry in filtered_data[memory_keys[0]] ]
    else:
        methods = []
    
    memories = sorted({ int(key.split('_')[1]) // 1000 for key in filtered_data.keys() })
    
    width = 0.15  
    x = np.arange(len(memories)) * 1.5 
    
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            memory_key = f"memory_{memory * 1000}_threshold_{threshold:.4f}"
            method_values = [entry[1][metric] for entry in filtered_data[memory_key] if entry[0] == method]
            avg_value = sum(method_values) / len(method_values) if method_values else None
            values.append(avg_value)
        
        overall_avg = np.mean([v for v in values if v is not None])
        if metric in ["Insert", "Query"]:
            print(f"{trace_label} - {method}: {short_title} average = {overall_avg:.3f} ms")
        else:
            print(f"{trace_label} - {method}: {short_title} average = {overall_avg:.3f}")
        
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
    plt.tight_layout()
    
    output_file = f'{trace_label}_{metric}_{threshold:.4f}_bar.png' if trace_label else f'{metric}_{threshold:.4f}_bar.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved bar chart to {output_file}")

def plot_line_chart(data, metric, short_title, threshold, markers, line_styles, trace_label="", font_size=14, figsize=(10, 6)):
    """Plot line chart (fixed threshold, comparing different memory and sketch methods)"""
    plt.figure(figsize=figsize)
    
    filtered_data = { key: val for key, val in data.items() if key.endswith(f"threshold_{threshold:.4f}") }
    
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    if memory_keys:
        methods = [ entry[0] for entry in filtered_data[memory_keys[0]] ]
    else:
        methods = []
    
    memories = sorted({ int(key.split('_')[1]) // 1000 for key in filtered_data.keys() })
    
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
    plt.tight_layout()
    
    output_file = f'{trace_label}_{metric}_{threshold:.4f}_line.png' if trace_label else f'{metric}_{threshold:.4f}_line.png'
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved line chart to {output_file}")

CAIDA2016 = {
    "memory_50000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.294628, "Query": 0.229649, "Recall": 0.784257, "Precision": 1.000000, "F1-score": 0.879085, "AAE": 210.837670, "ARE": 0.035387}),
        ("TightSketch", {"Insert": 0.331206, "Query": 0.237589, "Recall": 0.714286, "Precision": 1.000000, "F1-score": 0.833333, "AAE": 294.655782, "ARE": 0.048416}),
        ("StableSketch", {"Insert": 0.310333, "Query": 0.241013, "Recall": 0.563654, "Precision": 1.000000, "F1-score": 0.720945, "AAE": 88.474138, "ARE": 0.010038}),
        ("MVSketch", {"Insert": 0.352721, "Query": 0.332274, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260})
    ],

    "memory_100000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.284502, "Query": 0.230061, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 79.865564, "ARE": 0.013122}),
        ("TightSketch", {"Insert": 0.317620, "Query": 0.230657, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
        ("StableSketch", {"Insert": 0.306151, "Query": 0.238039, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
        ("MVSketch", {"Insert": 0.356080, "Query": 0.339518, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400})
    ],

    "memory_150000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.281130, "Query": 0.230607, "Recall": 0.968902, "Precision": 1.000000, "F1-score": 0.984205, "AAE": 38.585757, "ARE": 0.006777}),
        ("TightSketch", {"Insert": 0.302623, "Query": 0.224169, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 44.344097, "ARE": 0.008219}),
        ("StableSketch", {"Insert": 0.292950, "Query": 0.230008, "Recall": 0.734694, "Precision": 1.000000, "F1-score": 0.847059, "AAE": 155.871693, "ARE": 0.014521}),
        ("MVSketch", {"Insert": 0.349339, "Query": 0.348509, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095})
    ],
}

CAIDA2018 = {
    "memory_50000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.294628, "Query": 0.229649, "Recall": 0.784257, "Precision": 1.000000, "F1-score": 0.879085, "AAE": 210.837670, "ARE": 0.035387}),
        ("TightSketch", {"Insert": 0.331206, "Query": 0.237589, "Recall": 0.714286, "Precision": 1.000000, "F1-score": 0.833333, "AAE": 294.655782, "ARE": 0.048416}),
        ("StableSketch", {"Insert": 0.310333, "Query": 0.241013, "Recall": 0.563654, "Precision": 1.000000, "F1-score": 0.720945, "AAE": 88.474138, "ARE": 0.010038}),
        ("MVSketch", {"Insert": 0.352721, "Query": 0.332274, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260})
    ],

    "memory_100000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.284502, "Query": 0.230061, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 79.865564, "ARE": 0.013122}),
        ("TightSketch", {"Insert": 0.317620, "Query": 0.230657, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
        ("StableSketch", {"Insert": 0.306151, "Query": 0.238039, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
        ("MVSketch", {"Insert": 0.356080, "Query": 0.339518, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400})
    ],

    "memory_150000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.281130, "Query": 0.230607, "Recall": 0.968902, "Precision": 1.000000, "F1-score": 0.984205, "AAE": 38.585757, "ARE": 0.006777}),
        ("TightSketch", {"Insert": 0.302623, "Query": 0.224169, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 44.344097, "ARE": 0.008219}),
        ("StableSketch", {"Insert": 0.292950, "Query": 0.230008, "Recall": 0.734694, "Precision": 1.000000, "F1-score": 0.847059, "AAE": 155.871693, "ARE": 0.014521}),
        ("MVSketch", {"Insert": 0.349339, "Query": 0.348509, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095})
    ],
}

CAIDA2019 = {
    "memory_50000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.294628, "Query": 0.229649, "Recall": 0.784257, "Precision": 1.000000, "F1-score": 0.879085, "AAE": 210.837670, "ARE": 0.035387}),
        ("TightSketch", {"Insert": 0.331206, "Query": 0.237589, "Recall": 0.714286, "Precision": 1.000000, "F1-score": 0.833333, "AAE": 294.655782, "ARE": 0.048416}),
        ("StableSketch", {"Insert": 0.310333, "Query": 0.241013, "Recall": 0.563654, "Precision": 1.000000, "F1-score": 0.720945, "AAE": 88.474138, "ARE": 0.010038}),
        ("MVSketch", {"Insert": 0.352721, "Query": 0.332274, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260})
    ],

    "memory_100000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.284502, "Query": 0.230061, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 79.865564, "ARE": 0.013122}),
        ("TightSketch", {"Insert": 0.317620, "Query": 0.230657, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
        ("StableSketch", {"Insert": 0.306151, "Query": 0.238039, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
        ("MVSketch", {"Insert": 0.356080, "Query": 0.339518, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400})
    ],

    "memory_150000_threshold_0.0001": [
        ("MomentumSketch", {"Insert": 0.281130, "Query": 0.230607, "Recall": 0.968902, "Precision": 1.000000, "F1-score": 0.984205, "AAE": 38.585757, "ARE": 0.006777}),
        ("TightSketch", {"Insert": 0.302623, "Query": 0.224169, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 44.344097, "ARE": 0.008219}),
        ("StableSketch", {"Insert": 0.292950, "Query": 0.230008, "Recall": 0.734694, "Precision": 1.000000, "F1-score": 0.847059, "AAE": 155.871693, "ARE": 0.014521}),
        ("MVSketch", {"Insert": 0.349339, "Query": 0.348509, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095})
    ],
}

all_data_traces = [("CAIDA2016", CAIDA2016), ("CAIDA2018", CAIDA2018), ("CAIDA2019", CAIDA2019)]
threshold = 0.0001
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
line_styles = ['-', '--']

for trace_label, data in all_data_traces:
    plot_bar_chart(data, "Insert", "Insert", threshold, hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_bar_chart(data, "Query", "Query", threshold, hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))
    
    plot_line_chart(data, "AAE", "AAE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "ARE", "ARE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Recall", "Recall", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Precision", "Precision", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "F1-score", "F1-score", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
