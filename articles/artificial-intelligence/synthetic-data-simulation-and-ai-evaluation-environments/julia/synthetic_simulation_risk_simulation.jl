# Synthetic Data, Simulation, and AI Evaluation Environments
# Julia workflow for sim-to-real gap, rare-case coverage, and synthetic evaluation risk.
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

function simulate_synthetic_evaluations(; n::Int = 200, seed::Int = 42)
    Random.seed!(seed)

    fidelity_risk = rand(n) .* 0.30
    utility_gap = rand(n) .* 0.12
    privacy_risk = rand(n) .* 0.10
    rare_case_gap = rand(n) .* 0.12
    sim_to_real_gap = rand(n) .* 0.30
    benchmark_overfit = rand(n) .* 0.25

    evaluation_risk = clamp.(
        0.22 .* fidelity_risk .+
        0.18 .* utility_gap .+
        0.20 .* privacy_risk .+
        0.16 .* rare_case_gap .+
        0.16 .* sim_to_real_gap .+
        0.08 .* benchmark_overfit,
        0.0,
        1.0
    )

    return fidelity_risk, utility_gap, privacy_risk, rare_case_gap, sim_to_real_gap, benchmark_overfit, evaluation_risk
end

fidelity_risk, utility_gap, privacy_risk, rare_case_gap, sim_to_real_gap, benchmark_overfit, evaluation_risk = simulate_synthetic_evaluations()

open(joinpath(output_dir, "julia_synthetic_simulation_risk.csv"), "w") do io
    println(io, "case_id,fidelity_risk,utility_gap,privacy_risk,rare_case_gap,sim_to_real_gap,benchmark_overfit,evaluation_risk,review_required")
    for i in eachindex(evaluation_risk)
        review_required = evaluation_risk[i] > 0.12 ||
            privacy_risk[i] > 0.05 ||
            rare_case_gap[i] > 0.06 ||
            sim_to_real_gap[i] > 0.18

        @printf(
            io,
            "CASE-%03d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
            i,
            fidelity_risk[i],
            utility_gap[i],
            privacy_risk[i],
            rare_case_gap[i],
            sim_to_real_gap[i],
            benchmark_overfit[i],
            evaluation_risk[i],
            review_required ? "true" : "false"
        )
    end
end

open(joinpath(output_dir, "julia_synthetic_simulation_summary.csv"), "w") do io
    println(io, "mean_fidelity_risk,mean_utility_gap,mean_privacy_risk,mean_rare_case_gap,mean_sim_to_real_gap,mean_evaluation_risk,review_cases")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
        mean(fidelity_risk),
        mean(utility_gap),
        mean(privacy_risk),
        mean(rare_case_gap),
        mean(sim_to_real_gap),
        mean(evaluation_risk),
        sum(evaluation_risk .> 0.12)
    )
end

println("Julia synthetic simulation risk workflow complete.")
println("Mean evaluation risk: ", round(mean(evaluation_risk), digits = 4))
