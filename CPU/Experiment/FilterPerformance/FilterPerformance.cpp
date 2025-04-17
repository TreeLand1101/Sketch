#include "FilterBenchMark.h"

int main(int argc, char *argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << "./CPU <memory> <dataset1> <dataset2> ...\n";
        return 1;
    }

    uint32_t memory = std::stoi(argv[1]);

    for(uint32_t i = 2; i < argc; ++i) {
        std::cout << "+------------------------------------------------+" << std::endl;
        std::cout << argv[i] << std::endl;
        std::cout << "+------------------------------------------------+" << std::endl;
        FilterBenchMark dataset(argv[i], "Dataset");
        dataset.Bench<CMSketch<TUPLES, uint16_t>>(memory);
        dataset.Bench<CMSketch<TUPLES, uint16_t>>(memory, 2);
        dataset.Bench<CUSketch<TUPLES, uint16_t>>(memory);
        dataset.Bench<CUSketch<TUPLES, uint16_t>>(memory, 2);
    }
    return 0;
}
