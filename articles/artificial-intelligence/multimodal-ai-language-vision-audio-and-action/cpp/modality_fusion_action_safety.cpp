/*
Multimodal AI: Language, Vision, Audio, and Action

C++ example:
Modality-fusion scoring and action-safety thresholding.

Compile:
c++ -std=c++17 modality_fusion_action_safety.cpp -o modality_fusion_action_safety

Run:
./modality_fusion_action_safety
*/

#include <iostream>
#include <string>
#include <vector>

struct MultimodalCase {
    std::string id;
    double text_quality;
    double vision_quality;
    double audio_quality;
    double sensor_quality;
    double conflict_risk;
    double action_safety;
    bool action_requested;
};

double fusion_quality(const MultimodalCase& record) {
    return 0.30 * record.text_quality
        + 0.30 * record.vision_quality
        + 0.20 * record.audio_quality
        + 0.20 * record.sensor_quality
        - 0.20 * record.conflict_risk;
}

bool requires_review(const MultimodalCase& record) {
    double fusion = fusion_quality(record);

    if (fusion < 0.65) {
        return true;
    }

    if (record.conflict_risk > 0.35) {
        return true;
    }

    if (record.action_requested && record.action_safety < 0.80) {
        return true;
    }

    return false;
}

int main() {
    std::vector<MultimodalCase> cases = {
        {"MM-001", 0.90, 0.86, 0.70, 0.88, 0.10, 0.92, false},
        {"MM-002", 0.82, 0.52, 0.65, 0.76, 0.28, 0.91, false},
        {"MM-003", 0.88, 0.84, 0.80, 0.79, 0.44, 0.88, false},
        {"MM-004", 0.91, 0.87, 0.72, 0.85, 0.12, 0.62, true}
    };

    for (const auto& record : cases) {
        double fusion = fusion_quality(record);

        std::cout
            << record.id
            << " fusion_quality=" << fusion
            << " action_safety=" << record.action_safety
            << " review_required=" << (requires_review(record) ? "true" : "false")
            << "\n";
    }

    return 0;
}
