# Artificial Intelligence as a Systems Discipline
# Julia workflow for feedback-loop and lifecycle risk simulation.
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

function simulate_feedback_system(; periods::Int = 60, seed::Int = 42)
    Random.seed!(seed)

    data_quality = zeros(Float64, periods)
    model_performance = zeros(Float64, periods)
    governance_strength = zeros(Float64, periods)
    systemic_risk = zeros(Float64, periods)

    data_quality[1] = 0.75
    model_performance[1] = 0.72
    governance_strength[1] = 0.65

    for t in 2:periods
        feedback_pressure = 0.10 * (1.0 - governance_strength[t - 1])
        data_quality[t] = clamp(data_quality[t - 1] - feedback_pressure + randn() * 0.02, 0.0, 1.0)
        model_performance[t] = clamp(0.55 * model_performance[t - 1] + 0.45 * data_quality[t] + randn() * 0.02, 0.0, 1.0)
        governance_strength[t] = clamp(governance_strength[t - 1] + 0.01 - 0.03 * max(0.0, systemic_risk[t - 1] - 0.45), 0.0, 1.0)
        systemic_risk[t] = clamp(
            0.35 * (1.0 - data_quality[t]) +
            0.35 * (1.0 - model_performance[t]) +
            0.30 * (1.0 - governance_strength[t]),
            0.0,
            1.0
        )
    end

    return data_quality, model_performance, governance_strength, systemic_risk
end

data_quality, model_performance, governance_strength, systemic_risk = simulate_feedback_system()

open(joinpath(output_dir, "julia_feedback_loop_risk_simulation.csv"), "w") do io
    println(io, "period,data_quality,model_performance,governance_strength,systemic_risk")
    for t in eachindex(data_quality)
        @printf(
            io,
            "%d,%.6f,%.6f,%.6f,%.6f\n",
            t,
            data_quality[t],
            model_performance[t],
            governance_strength[t],
            systemic_risk[t]
        )
    end
end

open(joinpath(output_dir, "julia_feedback_loop_summary.csv"), "w") do io
    println(io, "mean_data_quality,mean_model_performance,mean_governance_strength,mean_systemic_risk")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f\n",
        mean(data_quality),
        mean(model_performance),
        mean(governance_strength),
        mean(systemic_risk)
    )
end

println("Julia feedback-loop risk simulation complete.")
println("Mean systemic risk: ", round(mean(systemic_risk), digits = 4))
