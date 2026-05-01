# Robustness and Adversarial Resilience in Machine Learning
# Julia workflow for perturbation, robustness, resilience, and risk simulation.
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

function simulate_resilience(; n::Int = 200, seed::Int = 42)
    Random.seed!(seed)

    clean_performance = rand(n) .* 0.18 .+ 0.80
    perturbation_budget = rand(n) .* 0.30
    adversarial_drop = clamp.(0.10 .+ 0.75 .* perturbation_budget .+ 0.05 .* randn(n), 0.0, 0.50)
    adversarial_performance = clamp.(clean_performance .- adversarial_drop, 0.0, 1.0)

    detection = rand(n) .* 0.45 .+ 0.45
    containment = rand(n) .* 0.45 .+ 0.45
    recovery = rand(n) .* 0.45 .+ 0.45
    exposure = rand(n)

    robustness_score = clamp.(1 .- adversarial_drop, 0.0, 1.0)
    resilience_score = 0.35 .* detection .+ 0.35 .* containment .+ 0.30 .* recovery

    system_risk = clamp.(
        0.30 .* (1 .- robustness_score) .+
        0.30 .* (1 .- resilience_score) .+
        0.40 .* exposure .* perturbation_budget,
        0.0,
        1.0
    )

    return clean_performance, perturbation_budget, adversarial_drop, adversarial_performance, detection, containment, recovery, exposure, robustness_score, resilience_score, system_risk
end

clean_performance, perturbation_budget, adversarial_drop, adversarial_performance, detection, containment, recovery, exposure, robustness_score, resilience_score, system_risk = simulate_resilience()

open(joinpath(output_dir, "julia_adversarial_resilience_simulation.csv"), "w") do io
    println(io, "case_id,clean_performance,perturbation_budget,adversarial_drop,adversarial_performance,detection,containment,recovery,exposure,robustness_score,resilience_score,system_risk")
    for i in eachindex(system_risk)
        @printf(
            io,
            "CASE-%03d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            i,
            clean_performance[i],
            perturbation_budget[i],
            adversarial_drop[i],
            adversarial_performance[i],
            detection[i],
            containment[i],
            recovery[i],
            exposure[i],
            robustness_score[i],
            resilience_score[i],
            system_risk[i]
        )
    end
end

open(joinpath(output_dir, "julia_adversarial_resilience_summary.csv"), "w") do io
    println(io, "mean_clean_performance,mean_adversarial_drop,mean_robustness_score,mean_resilience_score,mean_system_risk,review_cases")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
        mean(clean_performance),
        mean(adversarial_drop),
        mean(robustness_score),
        mean(resilience_score),
        mean(system_risk),
        sum(system_risk .> 0.42)
    )
end

println("Julia adversarial resilience simulation complete.")
println("Mean system risk: ", round(mean(system_risk), digits = 4))
