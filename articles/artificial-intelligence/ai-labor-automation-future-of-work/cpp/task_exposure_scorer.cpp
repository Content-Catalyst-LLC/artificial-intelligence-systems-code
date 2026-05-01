// High-throughput task exposure and redesign scoring example.

#include <iostream>
#include <vector>
#include <string>

double automation_pressure(double ai_capability, double routineness, double human_judgment) {
    return ai_capability * routineness * (1.0 - human_judgment);
}

double augmentation_potential(double ai_capability, double human_judgment, double task_value) {
    return ai_capability * human_judgment * task_value;
}

std::string classify_task(double automation, double augmentation, double human_judgment) {
    if (automation > 0.35 && human_judgment < 0.40) {
        return "candidate_for_careful_automation";
    } else if (augmentation > 0.35) {
        return "candidate_for_augmentation";
    } else if (human_judgment > 0.80) {
        return "protect_human_judgment";
    } else {
        return "redesign_with_monitoring";
    }
}

int main() {
    std::vector<std::string> tasks = {
        "document_summarization",
        "client_context_interpretation",
        "routine_data_entry"
    };

    std::vector<double> ai_capability = {0.85, 0.45, 0.90};
    std::vector<double> routineness = {0.70, 0.20, 0.90};
    std::vector<double> human_judgment = {0.35, 0.90, 0.20};
    std::vector<double> task_value = {0.65, 0.95, 0.40};

    for (size_t i = 0; i < tasks.size(); ++i) {
        double automation = automation_pressure(ai_capability[i], routineness[i], human_judgment[i]);
        double augmentation = augmentation_potential(ai_capability[i], human_judgment[i], task_value[i]);

        std::cout << tasks[i]
                  << " automation_pressure=" << automation
                  << " augmentation_potential=" << augmentation
                  << " category=" << classify_task(automation, augmentation, human_judgment[i])
                  << std::endl;
    }

    return 0;
}
