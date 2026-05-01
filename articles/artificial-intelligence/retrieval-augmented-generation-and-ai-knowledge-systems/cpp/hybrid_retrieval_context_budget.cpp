/*
Retrieval-Augmented Generation and AI Knowledge Systems

C++ example:
Hybrid retrieval scoring and context-budget selection.

Compile:
c++ -std=c++17 hybrid_retrieval_context_budget.cpp -o hybrid_retrieval_context_budget

Run:
./hybrid_retrieval_context_budget
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Chunk {
    std::string id;
    int tokens;
    double dense_similarity;
    double sparse_score;
    double authority_score;
    double freshness_score;
};

double hybrid_score(const Chunk& chunk) {
    return 0.40 * chunk.dense_similarity
        + 0.25 * chunk.sparse_score
        + 0.20 * chunk.authority_score
        + 0.15 * chunk.freshness_score;
}

int main() {
    int context_budget_tokens = 5000;
    int prompt_overhead_tokens = 1000;
    int reserved_output_tokens = 1200;
    int available_tokens = context_budget_tokens - prompt_overhead_tokens - reserved_output_tokens;

    std::vector<Chunk> chunks = {
        {"CHUNK-001", 700, 0.92, 0.64, 0.95, 0.88},
        {"CHUNK-002", 1300, 0.84, 0.92, 0.80, 0.70},
        {"CHUNK-003", 900, 0.76, 0.55, 0.98, 0.96},
        {"CHUNK-004", 1600, 0.66, 0.86, 0.60, 0.40},
        {"CHUNK-005", 600, 0.72, 0.74, 0.88, 0.91}
    };

    std::sort(
        chunks.begin(),
        chunks.end(),
        [](const Chunk& a, const Chunk& b) {
            return hybrid_score(a) > hybrid_score(b);
        }
    );

    int used_tokens = 0;

    std::cout << "Available evidence tokens: " << available_tokens << "\n";

    for (const auto& chunk : chunks) {
        bool selected = used_tokens + chunk.tokens <= available_tokens;

        std::cout
            << chunk.id
            << " hybrid_score=" << hybrid_score(chunk)
            << " tokens=" << chunk.tokens
            << " selected=" << (selected ? "true" : "false")
            << "\n";

        if (selected) {
            used_tokens += chunk.tokens;
        }
    }

    std::cout << "Used evidence tokens: " << used_tokens << "\n";

    return 0;
}
