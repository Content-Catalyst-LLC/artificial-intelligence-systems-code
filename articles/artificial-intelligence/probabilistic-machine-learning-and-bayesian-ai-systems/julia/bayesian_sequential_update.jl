# Probabilistic Machine Learning and Bayesian AI Systems
# Julia workflow for Bayesian sequential updating and uncertainty propagation.
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

function simulate_beta_updates(; periods::Int = 80, true_probability::Float64 = 0.18, seed::Int = 42)
    Random.seed!(seed)

    alpha = 2.0
    beta = 18.0

    posterior_mean = zeros(Float64, periods)
    posterior_sd = zeros(Float64, periods)
    observed_event = zeros(Int, periods)

    for t in 1:periods
        event = rand() < true_probability ? 1 : 0
        observed_event[t] = event

        alpha += event
        beta += 1 - event

        total = alpha + beta
        posterior_mean[t] = alpha / total
        posterior_sd[t] = sqrt((alpha * beta) / (total^2 * (total + 1)))
    end

    return observed_event, posterior_mean, posterior_sd
end

observed_event, posterior_mean, posterior_sd = simulate_beta_updates()

open(joinpath(output_dir, "julia_bayesian_sequential_update.csv"), "w") do io
    println(io, "period,observed_event,posterior_mean,posterior_sd,ci_lower,ci_upper")
    for i in eachindex(posterior_mean)
        ci_lower = max(0.0, posterior_mean[i] - 1.96 * posterior_sd[i])
        ci_upper = min(1.0, posterior_mean[i] + 1.96 * posterior_sd[i])

        @printf(
            io,
            "%d,%d,%.6f,%.6f,%.6f,%.6f\n",
            i,
            observed_event[i],
            posterior_mean[i],
            posterior_sd[i],
            ci_lower,
            ci_upper
        )
    end
end

open(joinpath(output_dir, "julia_bayesian_update_summary.csv"), "w") do io
    println(io, "final_posterior_mean,final_posterior_sd,observed_rate")
    @printf(
        io,
        "%.6f,%.6f,%.6f\n",
        posterior_mean[end],
        posterior_sd[end],
        mean(observed_event)
    )
end

println("Julia Bayesian sequential update complete.")
println("Final posterior mean: ", round(posterior_mean[end], digits = 4))
println("Final posterior sd: ", round(posterior_sd[end], digits = 4))
