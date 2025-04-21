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
    "memory_75000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.167950, "Query": 0.139450, "Recall": 0.402332, "Precision": 0.200387, "F1-score": 0.267528, "AAE": 6355.154589, "ARE": 0.967376}),
        ("Elastic", {"Insert": 0.088097, "Query": 0.078406, "Recall": 0.618076, "Precision": 0.806084, "F1-score": 0.699670, "AAE": 1562.849057, "ARE": 0.218279}),
        ("CocoSketch", {"Insert": 0.084840, "Query": 0.068036, "Recall": 0.741497, "Precision": 0.173016, "F1-score": 0.280566, "AAE": 1678.501966, "ARE": 0.326966}),
        ("StableSketch", {"Insert": 0.140305, "Query": 0.113408, "Recall": 0.624879, "Precision": 1.000000, "F1-score": 0.769139, "AAE": 198.108865, "ARE": 0.016661}),
        ("TightSketch", {"Insert": 0.148303, "Query": 0.112372, "Recall": 0.838678, "Precision": 1.000000, "F1-score": 0.912262, "AAE": 150.519119, "ARE": 0.026880}),
        ("MomentumSketch", {"Insert": 0.139875, "Query": 0.117106, "Recall": 0.900875, "Precision": 1.000000, "F1-score": 0.947853, "AAE": 108.320388, "ARE": 0.019546}),
        ("TwoStage", {"Insert": 0.074506, "Query": 0.090123, "Recall": 0.931001, "Precision": 0.901223, "F1-score": 0.915870, "AAE": 141.363257, "ARE": 0.027633})
    ],

    "memory_100000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.166286, "Query": 0.137567, "Recall": 0.521866, "Precision": 0.197572, "F1-score": 0.286629, "AAE": 3875.968343, "ARE": 0.687400}),
        ("Elastic", {"Insert": 0.082677, "Query": 0.070546, "Recall": 0.736638, "Precision": 0.807242, "F1-score": 0.770325, "AAE": 1094.941953, "ARE": 0.161874}),
        ("CocoSketch", {"Insert": 0.079537, "Query": 0.065921, "Recall": 0.836735, "Precision": 0.146678, "F1-score": 0.249601, "AAE": 944.269454, "ARE": 0.190132}),
        ("StableSketch", {"Insert": 0.147240, "Query": 0.114338, "Recall": 0.663751, "Precision": 1.000000, "F1-score": 0.797897, "AAE": 139.543192, "ARE": 0.014003}),
        ("TightSketch", {"Insert": 0.153731, "Query": 0.114423, "Recall": 0.909621, "Precision": 1.000000, "F1-score": 0.952672, "AAE": 86.378205, "ARE": 0.016077}),
        ("MomentumSketch", {"Insert": 0.143632, "Query": 0.110898, "Recall": 0.947522, "Precision": 1.000000, "F1-score": 0.973054, "AAE": 89.537436, "ARE": 0.013690}),
        ("TwoStage", {"Insert": 0.067052, "Query": 0.080129, "Recall": 0.980564, "Precision": 0.919781, "F1-score": 0.949200, "AAE": 88.616452, "ARE": 0.017836})
    ],

    "memory_125000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.156428, "Query": 0.130463, "Recall": 0.605442, "Precision": 0.182591, "F1-score": 0.280567, "AAE": 2702.016051, "ARE": 0.503618}),
        ("Elastic", {"Insert": 0.078472, "Query": 0.070798, "Recall": 0.820214, "Precision": 0.809981, "F1-score": 0.815065, "AAE": 830.319905, "ARE": 0.135894}),
        ("CocoSketch", {"Insert": 0.076196, "Query": 0.064652, "Recall": 0.894072, "Precision": 0.182467, "F1-score": 0.303080, "AAE": 669.688043, "ARE": 0.134901}),
        ("StableSketch", {"Insert": 0.144679, "Query": 0.116204, "Recall": 0.696793, "Precision": 1.000000, "F1-score": 0.821306, "AAE": 213.702929, "ARE": 0.017309}),
        ("TightSketch", {"Insert": 0.145649, "Query": 0.108757, "Recall": 0.947522, "Precision": 1.000000, "F1-score": 0.973054, "AAE": 61.153846, "ARE": 0.011376}),
        ("MomentumSketch", {"Insert": 0.133832, "Query": 0.111979, "Recall": 0.963071, "Precision": 1.000000, "F1-score": 0.981188, "AAE": 49.158426, "ARE": 0.008605}),
        ("TwoStage", {"Insert": 0.070754, "Query": 0.081737, "Recall": 0.995141, "Precision": 0.943779, "F1-score": 0.968780, "AAE": 67.704102, "ARE": 0.013586})
    ],

    "memory_150000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.170624, "Query": 0.142239, "Recall": 0.674441, "Precision": 0.170349, "F1-score": 0.271997, "AAE": 1920.936599, "ARE": 0.376095}),
        ("Elastic", {"Insert": 0.081776, "Query": 0.076709, "Recall": 0.874636, "Precision": 0.788091, "F1-score": 0.829111, "AAE": 614.186667, "ARE": 0.104478}),
        ("CocoSketch", {"Insert": 0.080078, "Query": 0.068617, "Recall": 0.919339, "Precision": 0.405660, "F1-score": 0.562928, "AAE": 488.646934, "ARE": 0.094753}),
        ("StableSketch", {"Insert": 0.140487, "Query": 0.112040, "Recall": 0.724976, "Precision": 1.000000, "F1-score": 0.840563, "AAE": 213.828418, "ARE": 0.019609}),
        ("TightSketch", {"Insert": 0.148687, "Query": 0.112748, "Recall": 0.967930, "Precision": 1.000000, "F1-score": 0.983704, "AAE": 42.941767, "ARE": 0.007680}),
        ("MomentumSketch", {"Insert": 0.136352, "Query": 0.110942, "Recall": 0.976676, "Precision": 1.000000, "F1-score": 0.988201, "AAE": 35.916418, "ARE": 0.006264}),
        ("TwoStage", {"Insert": 0.070377, "Query": 0.081938, "Recall": 1.000000, "Precision": 0.954545, "F1-score": 0.976744, "AAE": 49.963071, "ARE": 0.009916})
    ],

    "memory_175000_threshold_0.0001": [
        ("MVSketch", {"Insert": 0.170988, "Query": 0.145695, "Recall": 0.739553, "Precision": 0.169563, "F1-score": 0.275875, "AAE": 1393.942181, "ARE": 0.280528}),
        ("Elastic", {"Insert": 0.086235, "Query": 0.077685, "Recall": 0.921283, "Precision": 0.817241, "F1-score": 0.866149, "AAE": 540.572785, "ARE": 0.092383}),
        ("CocoSketch", {"Insert": 0.082672, "Query": 0.068899, "Recall": 0.938776, "Precision": 0.558059, "F1-score": 0.700000, "AAE": 364.534161, "ARE": 0.071126}),
        ("StableSketch", {"Insert": 0.141977, "Query": 0.113856, "Recall": 0.721088, "Precision": 1.000000, "F1-score": 0.837945, "AAE": 96.208895, "ARE": 0.011929}),
        ("TightSketch", {"Insert": 0.151626, "Query": 0.115759, "Recall": 0.979592, "Precision": 1.000000, "F1-score": 0.989691, "AAE": 35.153770, "ARE": 0.006607}),
        ("MomentumSketch", {"Insert": 0.135970, "Query": 0.111245, "Recall": 0.988338, "Precision": 1.000000, "F1-score": 0.994135, "AAE": 27.582104, "ARE": 0.004760}),
        ("TwoStage", {"Insert": 0.068469, "Query": 0.077295, "Recall": 0.999028, "Precision": 0.960748, "F1-score": 0.979514, "AAE": 40.730545, "ARE": 0.007966})
    ],

    # "memory_200000_threshold_0.0001": [
    #     ("MVSketch", {"Insert": 0.170371, "Query": 0.142697, "Recall": 0.788144, "Precision": 0.180946, "F1-score": 0.294320, "AAE": 1053.277435, "ARE": 0.218353}),
    #     ("Elastic", {"Insert": 0.083676, "Query": 0.077261, "Recall": 0.935860, "Precision": 0.799834, "F1-score": 0.862517, "AAE": 422.763240, "ARE": 0.073914}),
    #     ("CocoSketch", {"Insert": 0.080808, "Query": 0.068091, "Recall": 0.948494, "Precision": 0.679666, "F1-score": 0.791886, "AAE": 337.330943, "ARE": 0.061543}),
    #     ("StableSketch", {"Insert": 0.137510, "Query": 0.112739, "Recall": 0.743440, "Precision": 1.000000, "F1-score": 0.852843, "AAE": 197.568627, "ARE": 0.018802}),
    #     ("TightSketch", {"Insert": 0.141962, "Query": 0.113667, "Recall": 0.981535, "Precision": 1.000000, "F1-score": 0.990682, "AAE": 30.602970, "ARE": 0.005740}),
    #     ("MomentumSketch", {"Insert": 0.133682, "Query": 0.110989, "Recall": 0.982507, "Precision": 1.000000, "F1-score": 0.991176, "AAE": 24.881306, "ARE": 0.004436}),
    #     ("TwoStage", {"Insert": 0.067252, "Query": 0.075384, "Recall": 1.000000, "Precision": 0.966197, "F1-score": 0.982808, "AAE": 33.597668, "ARE": 0.006843})
    # ],
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

    plot_line_chart(data, "Insert", "Insert Time (ms)", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Query", "Query Time (ms)", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "AAE", "AAE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6), y_max=1500)
    plot_line_chart(data, "ARE", "ARE", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6), y_max=0.3)
    plot_line_chart(data, "Recall", "Recall", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "Precision", "Precision", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
    plot_line_chart(data, "F1-score", "F1-score", threshold, markers, line_styles, trace_label=trace_label, font_size=14, figsize=(10, 6))
