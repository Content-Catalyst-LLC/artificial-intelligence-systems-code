/*
Representation Learning and Embedding Spaces

C++ example:
High-performance cosine similarity and nearest-neighbor search.

Compile:
c++ -std=c++17 cosine_nearest_neighbor.cpp -o cosine_nearest_neighbor

Run:
./cosine_nearest_neighbor
*/

#include <cmath>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

struct EmbeddedObject {
    std::string id;
    std::vector<double> vector;
};

double dot_product(const std::vector<double>& a, const std::vector<double>& b) {
    double result = 0.0;

    for (size_t i = 0; i < a.size(); i++) {
        result += a[i] * b[i];
    }

    return result;
}

double norm(const std::vector<double>& a) {
    return std::sqrt(dot_product(a, a));
}

double cosine_similarity(const std::vector<double>& a, const std::vector<double>& b) {
    double denominator = norm(a) * norm(b);

    if (denominator == 0.0) {
        return 0.0;
    }

    return dot_product(a, b) / denominator;
}

int main() {
    std::vector<EmbeddedObject> objects = {
        {"D001", {0.82, 0.12, 0.08, 0.02}},
        {"D002", {0.79, 0.18, 0.10, 0.04}},
        {"D003", {0.05, 0.84, 0.11, 0.03}},
        {"D004", {0.02, 0.13, 0.88, 0.15}},
        {"D005", {0.04, 0.09, 0.16, 0.91}}
    };

    std::vector<double> query = {0.80, 0.15, 0.09, 0.03};

    std::string best_id;
    double best_similarity = -std::numeric_limits<double>::infinity();

    for (const auto& object : objects) {
        double similarity = cosine_similarity(query, object.vector);

        std::cout
            << object.id
            << " similarity="
            << similarity
            << "\n";

        if (similarity > best_similarity) {
            best_similarity = similarity;
            best_id = object.id;
        }
    }

    std::cout << "Nearest neighbor: " << best_id << "\n";
    std::cout << "Best similarity: " << best_similarity << "\n";

    return 0;
}
