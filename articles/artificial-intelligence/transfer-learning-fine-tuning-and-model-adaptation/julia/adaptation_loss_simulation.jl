# Transfer Learning, Fine-Tuning, and Model Adaptation
# Julia workflow for adaptation loss and forgetting-risk simulation.
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

function simulate_adaptation_curve(; steps::Int = 80, seed::Int = 42)
    Random.seed!(seed)

    target_loss = zeros(Float64, steps)
    source_retention = zeros(Float64, steps)
    adaptation_risk = zeros(Float64, steps)

    target_loss[1] = 1.0
    source_retention[1] = 0.96

    for t in 2:steps
        learning_gain = 0.035 * exp(-0.025 * t)
        overfit_pressure = max(0.0, (t - 45) / 80)

        target_loss[t] = max(0.15, target_loss[t - 1] - learning_gain + 0.015 * overfit_pressure + randn() * 0.005)
        source_retention[t] = clamp(source_retention[t - 1] - 0.003 - 0.006 * overfit_pressure + randn() * 0.003, 0.0, 1.0)
        adaptation_risk[t] = clamp(0.45 * (1.0 - source_retention[t]) + 0.35 * overfit_pressure + 0.20 * target_loss[t], 0.0, 1.0)
    end

    return target_loss, source_retention, adaptation_risk
end

target_loss, source_retention, adaptation_risk = simulate_adaptation_curve()

open(joinpath(output_dir, "julia_adaptation_loss_curve.csv"), "w") do io
    println(io, "step,target_loss,source_retention,adaptation_risk")
    for i in eachindex(target_loss)
        @printf(io, "%d,%.6f,%.6f,%.6f\n", i, target_loss[i], source_retention[i], adaptation_risk[i])
    end
end

open(joinpath(output_dir, "julia_adaptation_summary.csv"), "w") do io
    println(io, "final_target_loss,final_source_retention,final_adaptation_risk,mean_adaptation_risk")
    @printf(io, "%.6f,%.6f,%.6f,%.6f\n", target_loss[end], source_retention[end], adaptation_risk[end], mean(adaptation_risk))
end

println("Julia adaptation simulation complete.")
println("Final target loss: ", round(target_loss[end], digits = 4))
println("Final source retention: ", round(source_retention[end], digits = 4))
