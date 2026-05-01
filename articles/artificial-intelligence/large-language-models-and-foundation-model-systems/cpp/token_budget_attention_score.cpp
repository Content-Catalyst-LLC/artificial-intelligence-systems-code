/*
Large Language Models and Foundation Model Systems

C++ example:
Token-budget estimation and attention-style relevance scoring.

Compile:
c++ -std=c++17 token_budget_attention_score.cpp -o token_budget_attention_score

Run:
./token_budget_attention_score
*/

#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct ContextChunk {
    std::string id;
    int tokens;
    double query_similarity;
    double authority_score;
    double freshness_score;
};

double relevance_score(const ContextChunk& chunk) {
    return 0.50 * chunk.query_similarity
        + 0.30 * chunk.authority_score
        + 0.20 * chunk.freshness_score;
}

int main() {
    int context_budget = 6000;
    int system_prompt_tokens = 900;
    int user_prompt_tokens = 500;
    int reserved_output_tokens = 1200;

    int available_context_tokens =
        context_budget - system_prompt_tokens - user_prompt_tokens - reserved_output_tokens;

    std::vector<ContextChunk> chunks = {
        {"DOC-001", 900, 0.92, 0.95, 0.88},
        {"DOC-002", 1400, 0.84, 0.90, 0.60},
        {"DOC-003", 700, 0.78, 0.76, 0.92},
        {"DOC-004", 1600, 0.66, 0.98, 0.74}
    };

    std::cout << "Available context tokens: " << available_context_tokens << "\n";

    int used = 0;

    for (const auto& chunk : chunks) {
        double score = relevance_score(chunk);

        std::cout
            << chunk.id
            << " tokens=" << chunk.tokens
            << " relevance_score=" << score;

        if (used + chunk.tokens <= available_context_tokens) {
            used += chunk.tokens;
            std::cout << " selected=true";
        } else {
            std::cout << " selected=false";
        }

        std::cout << "\n";
    }

    std::cout << "Used context tokens: " << used << "\n";

    return 0;
}
