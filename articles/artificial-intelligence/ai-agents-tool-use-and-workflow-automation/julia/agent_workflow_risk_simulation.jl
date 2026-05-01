# AI Agents, Tool Use, and Workflow Automation
# Julia workflow for agent step-risk, tool-risk, and workflow utility simulation.
#
# Uses only Julia standard libraries.

using Random
using Statistics
using Printf

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

function simulate_agent_workflows(; n::Int = 200, seed::Int = 42)
    Random.seed!(seed)

    task_success = rand(n) .* 0.45 .+ 0.50
    permission_compliance = rand(n) .* 0.35 .+ 0.60
    safety_score = rand(n) .* 0.40 .+ 0.55
    auditability = rand(n) .* 0.40 .+ 0.55
    complexity = rand(n) .* 0.80 .+ 0.10
    tool_risk = rand(n) .* 0.55

    workflow_utility = 0.45 .* task_success .+
        0.20 .* permission_compliance .+
        0.20 .* safety_score .+
        0.15 .* auditability .-
        0.20 .* complexity .-
        0.20 .* tool_risk

    workflow_risk = clamp.(
        0.25 .* (1 .- task_success) .+
        0.25 .* (1 .- permission_compliance) .+
        0.20 .* (1 .- safety_score) .+
        0.15 .* complexity .+
        0.15 .* tool_risk,
        0.0,
        1.0
    )

    return task_success, permission_compliance, safety_score, auditability, complexity, tool_risk, workflow_utility, workflow_risk
end

task_success, permission_compliance, safety_score, auditability, complexity, tool_risk, workflow_utility, workflow_risk = simulate_agent_workflows()

open(joinpath(output_dir, "julia_agent_workflow_risk_simulation.csv"), "w") do io
    println(io, "case_id,task_success,permission_compliance,safety_score,auditability,complexity,tool_risk,workflow_utility,workflow_risk")
    for i in eachindex(workflow_risk)
        @printf(
            io,
            "CASE-%03d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            i,
            task_success[i],
            permission_compliance[i],
            safety_score[i],
            auditability[i],
            complexity[i],
            tool_risk[i],
            workflow_utility[i],
            workflow_risk[i]
        )
    end
end

open(joinpath(output_dir, "julia_agent_workflow_risk_summary.csv"), "w") do io
    println(io, "mean_task_success,mean_permission_compliance,mean_safety_score,mean_workflow_utility,mean_workflow_risk,high_risk_cases")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
        mean(task_success),
        mean(permission_compliance),
        mean(safety_score),
        mean(workflow_utility),
        mean(workflow_risk),
        sum(workflow_risk .> 0.42)
    )
end

println("Julia agent workflow risk simulation complete.")
println("Mean workflow risk: ", round(mean(workflow_risk), digits = 4))
