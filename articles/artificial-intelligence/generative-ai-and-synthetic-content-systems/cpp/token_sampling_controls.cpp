/*
Generative AI and Synthetic Content Systems

C++ example:
Token sampling with temperature control.

Compile:
c++ -std=c++17 token_sampling_controls.cpp -o token_sampling_controls

Run:
./token_sampling_controls
*/

#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

struct TokenLogit {
    std::string token;
    double logit;
    double probability;
};

std::vector<TokenLogit> softmax_with_temperature(std::vector<TokenLogit> tokens, double temperature) {
    double max_logit = tokens[0].logit;

    for (const auto& item : tokens) {
        max_logit = std::max(max_logit, item.logit);
    }

    double total = 0.0;

    for (auto& item : tokens) {
        item.probability = std::exp((item.logit - max_logit) / temperature);
        total += item.probability;
    }

    for (auto& item : tokens) {
        item.probability /= total;
    }

    std::sort(
        tokens.begin(),
        tokens.end(),
        [](const TokenLogit& a, const TokenLogit& b) {
            return a.probability > b.probability;
        }
    );

    return tokens;
}

int main() {
    std::vector<TokenLogit> tokens = {
        {"alpha", 3.2, 0.0},
        {"beta", 2.7, 0.0},
        {"gamma", 1.8, 0.0},
        {"delta", 0.9, 0.0},
        {"epsilon", 0.2, 0.0}
    };

    double temperatures[] = {0.50, 1.00, 1.50};

    for (double temperature : temperatures) {
        std::cout << "Temperature: " << temperature << "\n";

        auto probabilities = softmax_with_temperature(tokens, temperature);

        for (const auto& item : probabilities) {
            std::cout
                << item.token
                << " probability="
                << item.probability
                << "\n";
        }

        std::cout << "\n";
    }

    return 0;
}
