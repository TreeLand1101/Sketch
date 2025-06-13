#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("performance.csv")

# 1. Insert and Query Throughput vs Admission Ratio at memory ratio = 0.5:0.5
df_m = df[(df["Filter Ratio"] == 0.5) & (df["Sketch Ratio"] == 0.5)]
for metric, fname in [("Insert Throughput (Mops)", "insert_vs_admission.png"),
                      ("Query Throughput (Mops)", "query_vs_admission.png")]:
    plt.figure(figsize=(10,6))
    for ds in df_m["Dataset"].unique():
        sub = df_m[df_m["Dataset"] == ds]
        plt.plot(sub["Admission Ratio"], sub[metric], marker="o", linestyle="-", label=ds, alpha=0.7)
    plt.xlabel("Admission Ratio", fontsize=14)
    plt.ylabel(metric, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(loc="best", fontsize=12)
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()

# 2. F1 Score vs Memory Ratio at admission threshold = 0.9
df_f1 = df[df["Admission Ratio"] == 0.9]
plt.figure(figsize=(10,6))
for ds in df_f1["Dataset"].unique():
    sub = df_f1[df_f1["Dataset"] == ds]
    plt.plot(sub["Filter Ratio"], sub["F1 Score"], marker="o", linestyle="-", label=ds, alpha=0.7)
plt.xlabel("Filter Ratio (Memory Ratio)", fontsize=14)
plt.ylabel("F1 Score", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend(loc="best", fontsize=12)
plt.tight_layout()
plt.savefig("f1_vs_memory_ratio.png")
plt.close()
