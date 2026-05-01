/*
AI Agents, Tool Use, and Workflow Automation

C++ example:
Tool-risk scoring and permission-gated execution.

Compile:
c++ -std=c++17 tool_risk_permission_gate.cpp -o tool_risk_permission_gate

Run:
./tool_risk_permission_gate
*/

#include <iostream>
#include <string>
#include <vector>

struct ToolRequest {
    std::string request_id;
    std::string tool_name;
    std::string risk_level;
    double argument_validity;
    double permission_score;
    bool confirmation_required;
    bool confirmation_obtained;
};

double risk_weight(const std::string& risk_level) {
    if (risk_level == "read_only") return 0.05;
    if (risk_level == "compute") return 0.15;
    if (risk_level == "write") return 0.30;
    if (risk_level == "external_action") return 0.45;
    if (risk_level == "sensitive") return 0.55;
    return 0.60;
}

bool may_execute(const ToolRequest& request) {
    if (request.argument_validity < 0.70) {
        return false;
    }

    if (request.permission_score < 0.80) {
        return false;
    }

    if (request.confirmation_required && !request.confirmation_obtained) {
        return false;
    }

    if (request.risk_level == "sensitive" && request.permission_score < 0.95) {
        return false;
    }

    return true;
}

int main() {
    std::vector<ToolRequest> requests = {
        {"REQ-001", "search_docs", "read_only", 0.92, 0.94, false, true},
        {"REQ-002", "run_code", "compute", 0.81, 0.89, false, true},
        {"REQ-003", "update_ticket", "write", 0.87, 0.91, true, true},
        {"REQ-004", "send_external_email", "external_action", 0.88, 0.90, true, false},
        {"REQ-005", "query_sensitive_records", "sensitive", 0.90, 0.86, true, true}
    };

    for (const auto& request : requests) {
        double risk = risk_weight(request.risk_level);

        std::cout
            << request.request_id
            << " tool=" << request.tool_name
            << " risk_weight=" << risk
            << " execute=" << (may_execute(request) ? "true" : "false")
            << "\n";
    }

    return 0;
}
