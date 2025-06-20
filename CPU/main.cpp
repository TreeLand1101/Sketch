#include "BenchMark.h"

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << "./CPU <memory> <alpha> <dataset1> <dataset2> ...\n";
        return 1;
    }

    uint32_t memory = std::stoi(argv[1]);
    double alpha = std::stod(argv[2]);

    for(uint32_t i = 3; i < argc; ++i) {
        BenchMark dataset(argv[i]);

        /* PerformanceAll */
        // dataset.HHBench<MomentumSketch<TUPLES>>(memory, alpha);
        // dataset.HHBench<CMHeap<TUPLES>>(memory, alpha);
        // dataset.HHBench<SpaceSaving<TUPLES>>(memory, alpha);
        // dataset.HHBench<TwoStage<TUPLES>>(memory, alpha);        
        // dataset.HHBench<MVSketch<TUPLES>>(memory, alpha);
        // dataset.HHBench<Elastic<TUPLES>>(memory, alpha);
        // dataset.HHBench<CocoSketch<TUPLES>>(memory, alpha);
        // dataset.HHBench<TightSketch<TUPLES>>(memory, alpha);
        // dataset.HHBench<StableSketch<TUPLES>>(memory, alpha);

        /* PerformanceSIMD */
        // dataset.HHBench<MomentumSketchSIMD<TUPLES>>(memory, alpha);
        // dataset.HHBench<MomentumSketch<TUPLES>>(memory, alpha);

        /* PefromanceMomentumSketchVariant */
        dataset.HHBench<Default<TUPLES>>(memory, alpha);
        dataset.HHBench<Additive<TUPLES>>(memory, alpha);
        dataset.HHBench<MomentumOnly<TUPLES>>(memory, alpha);
        dataset.HHBench<CounterOnly<TUPLES>>(memory, alpha);
    }
    return 0;
}
