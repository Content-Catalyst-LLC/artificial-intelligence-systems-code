# Model Monitoring, Drift, and AI Observability
# Julia workflow for drift, performance decay, and alert simulation.
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

function simulate_observability(; n::Int = 24, seed::Int = 42)
    Random.seed!(seed)

    time_index = collect(1:n)

    feature_drift = clamp.(0.02 .+ 0.012 .* time_index .+ 0.03 .* randn(n), 0.0, 1.0)
    prediction_drift = clamp.(0.01 .+ 0.010 .* time_index .+ 0.03 .* randn(n), 0.0, 1.0)
    accuracy = clamp.(0.90 .- 0.006 .* time_index .+ 0.025 .* randn(n), 0.0, 1.0)
    latency = 350 .+ 18 .* time_index .+ 60 .* randn(n)
    incidents = rand(0:3, n)

    performance_degradation = clamp.(0.88 .- accuracy, 0.0, 1.0)

    observability_risk = clamp.(
        0.35 .* feature_drift .+
        0.25 .* prediction_drift .+
        0.25 .* performance_degradation .+
        0.10 .* clamp.(latency ./ 1200, 0.0, 1.0) .+
        0.05 .* clamp.(incidents ./ 3, 0.0, 1.0),
        0.0,
        1.0
    )

    return time_index, feature_drift, prediction_drift, accuracy, latency, incidents, observability_risk
end

time_index, feature_drift, prediction_drift, accuracy, latency, incidents, observability_risk = simulate_observability()

open(joinpath(output_dir, "julia_observability_simulation.csv"), "w") do io
    println(io, "batch,feature_drift,prediction_drift,accuracy,latency_ms,incident_count,observability_risk,review_required")
    for i in eachindex(time_index)
        review_required = observability_risk[i] > 0.25 || feature_drift[i] > 0.25 || accuracy[i] < 0.78 || incidents[i] >= 2

        @printf(
            io,
            "%d,%.6f,%.6f,%.6f,%.6f,%d,%.6f,%s\n",
            time_index[i],
            feature_drift[i],
            prediction_drift[i],
            accuracy[i],
            latency[i],
            incidents[i],
            observability_risk[i],
            review_required ? "true" : "false"
        )
    end
end

open(joinpath(output_dir, "julia_observability_summary.csv"), "w") do io
    println(io, "mean_feature_drift,mean_prediction_drift,minimum_accuracy,mean_latency_ms,mean_observability_risk,review_batches")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
        mean(feature_drift),
        mean(prediction_drift),
        minimum(accuracy),
        mean(latency),
        mean(observability_risk),
        sum(observability_risk .> 0.25)
    )
end

println("Julia observability simulation complete.")
println("Mean observability risk: ", round(mean(observability_risk), digits = 4))
