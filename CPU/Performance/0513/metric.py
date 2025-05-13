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

def plot_line_chart(data, metric, short_title, threshold, markers, line_styles, trace_label="", font_size=14, figsize=(10, 6), y_max=None):
    plt.figure(figsize=figsize)
    filtered_data = {k: v for k, v in data.items() if k.endswith(f"threshold_{threshold:.4f}")}
    memory_keys = sorted(filtered_data.keys(), key=lambda k: int(k.split('_')[1]))
    methods = [entry[0] for entry in filtered_data[memory_keys[0]]] if memory_keys else []
    memories = sorted({int(k.split('_')[1]) // 1000 for k in filtered_data})
    for i, method in enumerate(methods):
        values = []
        for memory in memories:
            key = f"memory_{memory * 1000}_threshold_{threshold:.4f}"
            val = next((e[1][metric] for e in filtered_data[key] if e[0] == method), None)
            values.append(val)
        style = line_styles[i % len(line_styles)]
        plt.plot(memories, values, marker=markers[i % len(markers)], linestyle=style, label=method, alpha=0.7, markersize=8)
    plt.xticks(memories, memories, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.xlabel("Memory (KB)", fontsize=font_size)
    plt.ylabel(short_title, fontsize=font_size)
    if y_max is not None:
        plt.ylim(0, y_max)
    elif metric in ["Recall", "Precision", "F1-score"]:
        plt.ylim(0, 1)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fontsize=font_size)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    output_file = f"{trace_label}_{metric}_{threshold:.4f}_line.png" if trace_label else f"{metric}_{threshold:.4f}_line.png"
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Saved line chart to {output_file}")


CAIDA2016 = {
    "memory_50000_threshold_0.0001": [
        ("MVSketch", {"Insert": 6.024430, "Query": 7.765940, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260}),
        ("Elastic", {"Insert": 10.735006, "Query": 13.894351, "Recall": 0.448008, "Precision": 0.792096, "F1-score": 0.572315, "AAE": 2483.477223, "ARE": 0.303714}),
        ("CocoSketch", {"Insert": 13.194628, "Query": 16.533598, "Recall": 0.607386, "Precision": 0.212585, "F1-score": 0.314941, "AAE": 3385.027200, "ARE": 0.630769}),
        ("TightSketch", {"Insert": 6.830302, "Query": 8.838263, "Recall": 0.715258, "Precision": 1.000000, "F1-score": 0.833994, "AAE": 344.831522, "ARE": 0.055440}),
        ("StableSketch", {"Insert": 6.898424, "Query": 8.918854, "Recall": 0.562682, "Precision": 1.000000, "F1-score": 0.720149, "AAE": 154.526770, "ARE": 0.012750}),
        ("MomentumSketch", {"Insert": 7.261927, "Query": 8.731873, "Recall": 0.782313, "Precision": 1.000000, "F1-score": 0.877863, "AAE": 213.732919, "ARE": 0.035894}),
        ("TwoStage", {"Insert": 12.673771, "Query": 10.443607, "Recall": 0.718173, "Precision": 0.906748, "F1-score": 0.801518, "AAE": 360.458728, "ARE": 0.059723})
    ],

    "memory_75000_threshold_0.0001": [
        ("MVSketch", {"Insert": 6.221490, "Query": 7.667350, "Recall": 0.402332, "Precision": 0.200387, "F1-score": 0.267528, "AAE": 6355.154589, "ARE": 0.967376}),
        ("Elastic", {"Insert": 12.049863, "Query": 14.856592, "Recall": 0.618076, "Precision": 0.806084, "F1-score": 0.699670, "AAE": 1562.849057, "ARE": 0.218279}),
        ("CocoSketch", {"Insert": 12.723206, "Query": 15.770011, "Recall": 0.750243, "Precision": 0.175057, "F1-score": 0.283876, "AAE": 1696.484456, "ARE": 0.331825}),
        ("TightSketch", {"Insert": 6.796109, "Query": 9.455965, "Recall": 0.831876, "Precision": 1.000000, "F1-score": 0.908223, "AAE": 145.133178, "ARE": 0.025724}),
        ("StableSketch", {"Insert": 7.372509, "Query": 8.982033, "Recall": 0.628766, "Precision": 1.000000, "F1-score": 0.772076, "AAE": 162.749614, "ARE": 0.015773}),
        ("MomentumSketch", {"Insert": 7.250595, "Query": 8.757726, "Recall": 0.884354, "Precision": 1.000000, "F1-score": 0.938628, "AAE": 121.029670, "ARE": 0.018788}),
        ("TwoStage", {"Insert": 13.871141, "Query": 11.583262, "Recall": 0.932945, "Precision": 0.901408, "F1-score": 0.916905, "AAE": 142.056250, "ARE": 0.027640})
    ],

    "memory_100000_threshold_0.0001": [
        ("MVSketch", {"Insert": 6.062370, "Query": 7.446290, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400}),
        ("Elastic", {"Insert": 11.984691, "Query": 14.624700, "Recall": 0.736638, "Precision": 0.807242, "F1-score": 0.770325, "AAE": 1094.941953, "ARE": 0.161874}),
        ("CocoSketch", {"Insert": 12.779560, "Query": 15.254449, "Recall": 0.846453, "Precision": 0.148356, "F1-score": 0.252464, "AAE": 985.800230, "ARE": 0.194897}),
        ("TightSketch", {"Insert": 6.747759, "Query": 9.121569, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 87.136120, "ARE": 0.016272}),
        ("StableSketch", {"Insert": 7.352423, "Query": 9.376116, "Recall": 0.686103, "Precision": 1.000000, "F1-score": 0.813833, "AAE": 146.249292, "ARE": 0.015382}),
        ("MomentumSketch", {"Insert": 7.692966, "Query": 8.951552, "Recall": 0.953353, "Precision": 1.000000, "F1-score": 0.976119, "AAE": 72.039755, "ARE": 0.012574}),
        ("TwoStage", {"Insert": 14.153718, "Query": 11.679674, "Recall": 0.979592, "Precision": 0.919708, "F1-score": 0.948706, "AAE": 88.395833, "ARE": 0.017781})
    ],

    "memory_125000_threshold_0.0001": [
        ("MVSketch", {"Insert": 6.022940, "Query": 7.249720, "Recall": 0.605442, "Precision": 0.182591, "F1-score": 0.280567, "AAE": 2702.016051, "ARE": 0.503618}),
        ("Elastic", {"Insert": 11.842075, "Query": 14.164647, "Recall": 0.820214, "Precision": 0.809981, "F1-score": 0.815065, "AAE": 830.319905, "ARE": 0.135894}),
        ("CocoSketch", {"Insert": 12.168683, "Query": 14.815088, "Recall": 0.888241, "Precision": 0.180205, "F1-score": 0.299623, "AAE": 640.817287, "ARE": 0.126540}),
        ("TightSketch", {"Insert": 6.615575, "Query": 9.182888, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 61.577042, "ARE": 0.011390}),
        ("StableSketch", {"Insert": 7.480634, "Query": 9.383278, "Recall": 0.716229, "Precision": 1.000000, "F1-score": 0.834655, "AAE": 143.382632, "ARE": 0.014109}),
        ("MomentumSketch", {"Insert": 7.698030, "Query": 8.683162, "Recall": 0.961127, "Precision": 1.000000, "F1-score": 0.980178, "AAE": 60.572295, "ARE": 0.009929}),
        ("TwoStage", {"Insert": 14.095634, "Query": 12.268712, "Recall": 0.995141, "Precision": 0.943779, "F1-score": 0.968780, "AAE": 67.694336, "ARE": 0.013583})
    ],
}

# CAIDA2018 = {
#     "memory_50000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.294628, "Query": 0.229649, "Recall": 0.784257, "Precision": 1.000000, "F1-score": 0.879085, "AAE": 210.837670, "ARE": 0.035387}),
#         ("TightSketch", {"Insert": 0.331206, "Query": 0.237589, "Recall": 0.714286, "Precision": 1.000000, "F1-score": 0.833333, "AAE": 294.655782, "ARE": 0.048416}),
#         ("StableSketch", {"Insert": 0.310333, "Query": 0.241013, "Recall": 0.563654, "Precision": 1.000000, "F1-score": 0.720945, "AAE": 88.474138, "ARE": 0.010038}),
#         ("MVSketch", {"Insert": 0.352721, "Query": 0.332274, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260})
#     ],

#     "memory_100000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.284502, "Query": 0.230061, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 79.865564, "ARE": 0.013122}),
#         ("TightSketch", {"Insert": 0.317620, "Query": 0.230657, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
#         ("StableSketch", {"Insert": 0.306151, "Query": 0.238039, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
#         ("MVSketch", {"Insert": 0.356080, "Query": 0.339518, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400})
#     ],

#     "memory_150000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.281130, "Query": 0.230607, "Recall": 0.968902, "Precision": 1.000000, "F1-score": 0.984205, "AAE": 38.585757, "ARE": 0.006777}),
#         ("TightSketch", {"Insert": 0.302623, "Query": 0.224169, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 44.344097, "ARE": 0.008219}),
#         ("StableSketch", {"Insert": 0.292950, "Query": 0.230008, "Recall": 0.734694, "Precision": 1.000000, "F1-score": 0.847059, "AAE": 155.871693, "ARE": 0.014521}),
#         ("MVSketch", {"Insert": 0.349339, "Query": 0.348509, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095})
#     ],
# }

# CAIDA2019 = {
#     "memory_50000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.294628, "Query": 0.229649, "Recall": 0.784257, "Precision": 1.000000, "F1-score": 0.879085, "AAE": 210.837670, "ARE": 0.035387}),
#         ("TightSketch", {"Insert": 0.331206, "Query": 0.237589, "Recall": 0.714286, "Precision": 1.000000, "F1-score": 0.833333, "AAE": 294.655782, "ARE": 0.048416}),
#         ("StableSketch", {"Insert": 0.310333, "Query": 0.241013, "Recall": 0.563654, "Precision": 1.000000, "F1-score": 0.720945, "AAE": 88.474138, "ARE": 0.010038}),
#         ("MVSketch", {"Insert": 0.352721, "Query": 0.332274, "Recall": 0.292517, "Precision": 0.222798, "F1-score": 0.252941, "AAE": 12385.063123, "ARE": 1.785260})
#     ],

#     "memory_100000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.284502, "Query": 0.230061, "Recall": 0.939747, "Precision": 1.000000, "F1-score": 0.968938, "AAE": 79.865564, "ARE": 0.013122}),
#         ("TightSketch", {"Insert": 0.317620, "Query": 0.230657, "Recall": 0.906706, "Precision": 1.000000, "F1-score": 0.951070, "AAE": 84.231511, "ARE": 0.015558}),
#         ("StableSketch", {"Insert": 0.306151, "Query": 0.238039, "Recall": 0.679300, "Precision": 1.000000, "F1-score": 0.809028, "AAE": 155.566524, "ARE": 0.015543}),
#         ("MVSketch", {"Insert": 0.356080, "Query": 0.339518, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400})
#     ],

#     "memory_150000_threshold_0.0001": [
#         ("MomentumSketch", {"Insert": 0.281130, "Query": 0.230607, "Recall": 0.968902, "Precision": 1.000000, "F1-score": 0.984205, "AAE": 38.585757, "ARE": 0.006777}),
#         ("TightSketch", {"Insert": 0.302623, "Query": 0.224169, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 44.344097, "ARE": 0.008219}),
#         ("StableSketch", {"Insert": 0.292950, "Query": 0.230008, "Recall": 0.734694, "Precision": 1.000000, "F1-score": 0.847059, "AAE": 155.871693, "ARE": 0.014521}),
#         ("MVSketch", {"Insert": 0.349339, "Query": 0.348509, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095})
#     ],
# }

all_data_traces = [
    ("CAIDA2016", CAIDA2016), 
    # ("CAIDA2018", CAIDA2018), 
    # ("CAIDA2019", CAIDA2019)
]

threshold = 0.0001
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', 'x', '+']
hatch_patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
line_styles = ['-', '--']

for trace_label, data in all_data_traces:
    # plot_bar_chart(data, "Insert", "Insert", threshold, hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))
    # plot_bar_chart(data, "Query", "Query", threshold, hatch_patterns, trace_label=trace_label, font_size=14, figsize=(10, 6))

    plot_line_chart(data, "Insert", "Mops", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Query", "Mops", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "AAE", "AAE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6), y_max=1500)
    plot_line_chart(data, "ARE", "ARE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6), y_max=0.3)
    plot_line_chart(data, "Recall", "Recall", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Precision", "Precision", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "F1-score", "F1-score", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
