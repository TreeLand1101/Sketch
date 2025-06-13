import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

LABEL_SIZE  = 18
TICK_SIZE   = 12
# LEGEND_SIZE = 14 

df = pd.read_csv("performance.csv")
df["Memory Ratio"] = df["Filter Ratio"].astype(str) + ":" + df["Sketch Ratio"].astype(str)

metrics = [
    ("F1 Score",                   "YlOrRd", "heatmap_f1.png",      "F1 Score Heatmap"),
    ("Precision",                  "YlOrRd", "heatmap_precision.png", "Precision Heatmap"),
    ("Recall",                     "YlOrRd", "heatmap_recall.png",    "Recall Heatmap"),
    ("Insert Throughput (Mops)",   "YlGnBu", "heatmap_insert.png",    "Insert Throughput Heatmap"),
    ("Query Throughput (Mops)",    "YlGnBu", "heatmap_query.png",     "Query Throughput Heatmap"),
]

for metric, cmap, filename, title in metrics:
    pivot_table = df.pivot(index="Memory Ratio", columns="Admission Ratio", values=metric)

    plt.figure(figsize=(8, 6), constrained_layout=True)
    ax = sns.heatmap(
        pivot_table,
        annot=True,
        fmt=".2f",
        cmap=cmap
    )

    ax.set_xlabel("Admission ratio α",  fontsize=LABEL_SIZE)
    ax.set_ylabel("Meomory ratio (γ:1-γ)", fontsize=LABEL_SIZE)
    ax.tick_params(axis='both',       labelsize=TICK_SIZE)

    plt.savefig(filename, bbox_inches='tight')
    plt.clf()
    print(f"Saved {filename}")
