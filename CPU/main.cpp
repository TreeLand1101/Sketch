#include "BenchMark.h"

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << "./CPU <memory> <threshold> <dataset1> <dataset2> ...\n";
        return 1;
    }

    uint32_t memory = std::stoi(argv[1]);
    double threshold = std::stod(argv[2]);

    for(uint32_t i = 3; i < argc; ++i) {
        std::cout << "+------------------------------------------------+" << std::endl;
        std::cout << argv[i] << std::endl;
        std::cout << "+------------------------------------------------+" << std::endl;
        BenchMark dataset(argv[i], "Dataset");
        dataset.HHBench<MVSketch<TUPLES>>(memory, threshold);
        dataset.HHBench<Elastic<TUPLES>>(memory, threshold);
        dataset.HHBench<CocoSketch<TUPLES>>(memory, threshold);
        dataset.HHBench<TightSketch<TUPLES>>(memory, threshold);
        dataset.HHBench<StableSketch<TUPLES>>(memory, threshold);
        dataset.HHBench<MomentumSketch<TUPLES>>(memory, threshold);
        dataset.HHBench<TwoStage<TUPLES>>(memory, threshold);
    }
    return 0;
}
