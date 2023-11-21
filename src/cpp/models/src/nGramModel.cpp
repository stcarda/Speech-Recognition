#include "../include/models.hpp"

NGramModel::NGramModel(uint8_t N) {
    if (N == 0) {
        throw std::invalid_argument(
            "Cannot process N-Gram with parameter 0."
        );
    }
    this->N = N;
}