/*
Self-Supervised Learning and Foundation Models

C++ example:
Contrastive similarity scoring for representation evaluation.

Compile:
c++ -std=c++17 contrastive_similarity_scoring.cpp -o contrastive_similarity_scoring

Run:
./contrastive_similarity_scoring
*/

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct PairScore {
    std::string pair_id;
    double positive_similarity;
    double negative_similarity;
    double temperature;
};

double contrastive_margin(double positive_similarity, double negative_similarity) {
    return positive_similarity - negative_similarity;
}

double softmax_positive_probability(double positive_similarity, double negative_similarity, double temperature) {
    double pos = std::exp(positive_similarity / temperature);
    double neg = std::exp(negative_similarity / temperature);
    return pos / (pos + neg);
}

int main() {
    std::vector<PairScore> pairs = {
        {"P001", 0.82, 0.25, 0.10},
        {"P002", 0.76, 0.48, 0.10},
        {"P003", 0.64, 0.59, 0.10},
        {"P004", 0.91, 0.18, 0.10}
    };

    for (const auto& pair : pairs) {
        double margin = contrastive_margin(pair.positive_similarity, pair.negative_similarity);
        double probability = softmax_positive_probability(
            pair.positive_similarity,
            pair.negative_similarity,
            pair.temperature
        );

        std::cout
            << pair.pair_id
            << " margin=" << margin
            << " positive_probability=" << probability
            << "\n";
    }

    return 0;
}
