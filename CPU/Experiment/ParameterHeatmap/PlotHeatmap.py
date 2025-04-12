import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("heatmap_results.csv")

df["MemoryRatio"] = df["FilterRatio"].astype(str) + "/" + df["SketchRatio"].astype(str)

pivot_f1 = df.pivot(index="MemoryRatio", columns="AdmissionRatio", values="F1score")
pivot_precision = df.pivot(index="MemoryRatio", columns="AdmissionRatio", values="Precision")
pivot_recall = df.pivot(index="MemoryRatio", columns="AdmissionRatio", values="Recall")
pivot_insert = df.pivot(index="MemoryRatio", columns="AdmissionRatio", values="InsertTime")
pivot_query = df.pivot(index="MemoryRatio", columns="AdmissionRatio", values="QueryTime")

plt.figure(figsize=(8,6))
sns.heatmap(pivot_f1, annot=True, cmap="YlOrRd")
plt.title("F1score Heatmap")
plt.xlabel("AdmissionRatio")
plt.ylabel("Memory Ratio (Filter/Sketch)")
plt.savefig("heatmap_f1.png")
plt.clf()

plt.figure(figsize=(8,6))
sns.heatmap(pivot_precision, annot=True, cmap="YlOrRd")
plt.title("Precision Heatmap")
plt.xlabel("AdmissionRatio")
plt.ylabel("Memory Ratio (Filter/Sketch)")
plt.savefig("heatmap_precision.png")
plt.clf()

plt.figure(figsize=(8,6))
sns.heatmap(pivot_recall, annot=True, cmap="YlOrRd")
plt.title("Recall Heatmap")
plt.xlabel("AdmissionRatio")
plt.ylabel("Memory Ratio (Filter/Sketch)")
plt.savefig("heatmap_recall.png")
plt.clf()

plt.figure(figsize=(8,6))
sns.heatmap(pivot_insert, annot=True, cmap="YlGnBu_r")
plt.title("Insert Time Heatmap (Lower is Hot)")
plt.xlabel("AdmissionRatio")
plt.ylabel("Memory Ratio (Filter/Sketch)")
plt.savefig("heatmap_insert.png")
plt.clf()

plt.figure(figsize=(8,6))
sns.heatmap(pivot_query, annot=True, cmap="YlGnBu_r")
plt.title("Query Time Heatmap (Lower is Hot)")
plt.xlabel("AdmissionRatio")
plt.ylabel("Memory Ratio (Filter/Sketch)")
plt.savefig("heatmap_query.png")
plt.clf()
