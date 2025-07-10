# Momentum-Sketch and Two-Stage Framework

## Introduction
We propose a Two-Stage framework to enhance the efficiency and scalability of heavy hitter detection. 

In Stage 1, incoming packets are inserted into a two-row CU Sketch, serving as a high-throughput pre-filter that quickly discards most low-volume flows with minimal memory and per-packet overhead. Flows exceeding an admission threshold are forwarded to Stage 2. 

In Stage 2, we introduce Momentum-Sketch, a novel counting data structure that combines arrival strength with estimated frequency via a momentum metric and employs a probabilistic counter-decay strategy to preferentially retain true heavy hitters, effectively reducing estimation errors under skewed distributions. Momentum-Sketch is further enhanced with SIMD instructions to accelerate insert and query operations.

## Experimental Results
Momentum-Sketch excels in accuracy under low memory budgets. At 16 KB, its average F1 score across all datasets surpasses that of CM Heap, Space-Saving, MV-Sketch, Elastic Sketch, CocoSketch, Tight-Sketch, and Stable-Sketch by approximately 481%, 520%, 274%, 104%, 124%, 10%, and 13%, respectively. 

Momentum-Sketch further enhances its performance by leveraging SIMD acceleration, significantly boosting both insert and query speeds. It boosts average insert throughput by 43%, 37%, and 62% on the CAIDA 2016, MAWI 2021, and Campus datasets, respectively. Similarly, it improves average query throughput by 50%, 39%, and 99% on the CAIDA 2016, MAWI 2021, and Campus datasets, respectively.

The Two-Stage framework improves the average insert throughput by 69.47%, 51.88%, 54.89%, 27.71%, 30.65%, and 124.24% on the CAIDA 2016, CAIDA 2018, CAIDA 2019, MAWI 2021, MAWI 2022, and Campus datasets, respectively. Furthermore, it enhances the average query throughput by 20.98%, 10.90%, 10.71%, 2.56%, 6.16%, and 101.83% on the same datasets.

In conclusion, Momentum-Sketch is highly effective in resource-constrained scenarios, delivering exceptional F1 scores at memory sizes ranging from 16 KB to 128 KB. Conversely, the Two-Stage framework significantly improves throughput while maintaining a high F1 score at memory sizes of 128 KB and beyond, making it an excellent choice for systems with greater memory capacity.

## 簡介
我們提出Two-Stage 架構，以提升重點流量檢測的效率與可擴展性。

在第一階段 (Stage 1)，輸入資料封包被插入至一個 two-row CU Sketch，作為高吞吐量的預過濾器，快速剔除大多數低流量，以最小的記憶體與每封包開銷實現過濾。超過准入閾值 (admission threshold) 的流量被轉發至第二階段 (Stage 2)。

在第二階段，我們提出 Momentum-Sketch計數資料結構，透過動量指標 (momentum metric) 結合到達強度 (arrival strength) 與估計頻率，並採用機率計數器衰減策略 (probabilistic counter-decay strategy)，優先保留真正的重點流量，有效降低偏態分佈下的估計誤差。Momentum-Sketch 進一步利用 SIMD 指令加速插入與查詢操作。

## 實驗結果
Momentum-Sketch 在低記憶體預算下表現卓越。在 16 KB 的記憶體下，其在所有資料集上的平均 F1 score 比 CM Heap、Space-Saving、MV-Sketch、Elastic Sketch、CocoSketch、Tight-Sketch 和 Stable-Sketch 分別高出約 481%、520%、274%、104%、124%、10% 和 13%。

Momentum-Sketch 通過利用 SIMD 加速技術進一步提升了性能，顯著提高了 insert 和 query 速度。它在 CAIDA 2016、MAWI 2021 和 Campus 資料集上的平均 insert throughput 分別提高了 43%、37% 和 62%。同樣地，它在 CAIDA 2016、MAWI 2021 和 Campus 資料集上的平均 query throughput 分別提高了 50%、39% 和 99%。

Two-Stage 框架透過過濾低流量，大幅提升了 insert 和 query throughput，同時保持了高 F1 score。具體來說，它在 CAIDA 2016、CAIDA 2018、CAIDA 2019、MAWI 2021、MAWI 2022 和 Campus 資料集上的平均insert throughput 比 Momentum-Sketch 分別提高了 69.47%、51.88%、54.89%、27.71%、30.65% 和 124.24%。此外，它在這些資料集上的平均query throughput 也分別提高了 20.98%、10.90%、10.71%、2.56%、6.16% 和 101.83%。

綜上所述，Momentum-Sketch 在資源有限的情況下表現出色，在 16 KB 到 128 KB 的記憶體下提供了卓越的 F1 score。而Two-Stage 框架在 128 KB 及以上的記憶體下顯著提升 throughput 並維持高 F1 score，使其成為記憶體容量較大系統的選擇。