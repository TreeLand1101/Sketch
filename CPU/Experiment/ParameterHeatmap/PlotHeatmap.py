import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("heatmap_results.csv")

df["Memory Ratio"] = df["Filter Ratio"].astype(str) + ":" + df["Sketch Ratio"].astype(str)

metrics = [
    ("F1 Score", "YlOrRd", "heatmap_f1.png", "F1 Score Heatmap"),
    ("Precision", "YlOrRd", "heatmap_precision.png", "Precision Heatmap"),
    ("Recall", "YlOrRd", "heatmap_recall.png", "Recall Heatmap"),
    ("Insert Throughput (Mops)", "YlGnBu", "heatmap_insert.png", "Insert Throughput Heatmap"),
    ("Query Throughput (Mops)", "YlGnBu", "heatmap_query.png", "Query Throughput Heatmap"),
]

for metric, cmap, filename, title in metrics:
    pivot_table = df.pivot(index="Memory Ratio", columns="Admission Ratio", values=metric)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        pivot_table,
        annot=True,
        fmt=".2f",  
        cmap=cmap
    )
    plt.title(title)
    plt.xlabel("Admission Ratio")
    plt.ylabel("Memory Ratio (Filter : Main)")
    plt.tight_layout()
    plt.savefig(filename)
    plt.clf()
