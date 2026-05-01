# AI Safety and System Reliability
# Julia workflow for stochastic reliability simulation and threshold tradeoff analysis.
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

sigmoid(x) = 1.0 / (1.0 + exp(-x))

function simulate_events(n::Int; seed::Int = 42, shift::Float64 = 0.0)
    Random.seed!(seed)

    asset_age = max.(randn(n) .* 3.0 .+ 10.0 .+ shift, 0.0)
    sensor_load = clamp.(randn(n) .* 0.15 .+ 0.50 .+ 0.03 * shift, 0.0, 1.0)
    maintenance_gap = max.(randn(n) .* 30.0 .+ 90.0 .+ 8.0 * shift, 0.0)

    latent_risk = -3.0 .+
        0.12 .* asset_age .+
        2.4 .* sensor_load .+
        0.014 .* maintenance_gap .+
        randn(n) .* 0.35

    predicted_probability = sigmoid.(latent_risk)

    uncertainty = clamp.(
        0.08 .+
        0.38 .* exp.(-((predicted_probability .- 0.50) .^ 2) ./ 0.035) .+
        0.03 * abs(shift) .+
        randn(n) .* 0.02,
        0.0,
        1.0
    )

    observed_outcome = rand(n) .< predicted_probability

    return (
        asset_age = asset_age,
        sensor_load = sensor_load,
        maintenance_gap = maintenance_gap,
        predicted_probability = predicted_probability,
        uncertainty = uncertainty,
        observed_outcome = observed_outcome
    )
end

function threshold_sweep(events; uncertainty_threshold::Float64 = 0.30)
    thresholds = collect(0.10:0.05:0.90)
    rows = Vector{NamedTuple}()

    for threshold in thresholds
        flagged = events.predicted_probability .>= threshold
        review_required = events.uncertainty .> uncertainty_threshold
        missed_failure = .!flagged .& events.observed_outcome

        push!(
            rows,
            (
                decision_threshold = threshold,
                flag_rate = mean(flagged),
                review_rate = mean(review_required),
                missed_failure_rate = mean(missed_failure),
                mean_uncertainty = mean(events.uncertainty)
            )
        )
    end

    return rows
end

function simulate_reliability_curve(n_systems::Int; seed::Int = 303, horizon::Int = 180)
    Random.seed!(seed)

    shape = 1.8
    scale = 120.0

    uniform_draws = rand(n_systems)
    incident_times = scale .* (-log.(1.0 .- uniform_draws)) .^ (1.0 / shape)

    early_failure = rand(n_systems) .< 0.05
    incident_times[early_failure] .= rand(sum(early_failure)) .* 19.0 .+ 1.0

    rows = Vector{NamedTuple}()

    for day in 1:horizon
        reliability = mean(incident_times .> day)
        push!(
            rows,
            (
                day = day,
                reliability = reliability,
                cumulative_failure_probability = 1.0 - reliability
            )
        )
    end

    return rows
end

function write_threshold_sweep(path::String, rows)
    open(path, "w") do io
        println(io, "decision_threshold,flag_rate,review_rate,missed_failure_rate,mean_uncertainty")
        for row in rows
            @printf(
                io,
                "%.2f,%.6f,%.6f,%.6f,%.6f\n",
                row.decision_threshold,
                row.flag_rate,
                row.review_rate,
                row.missed_failure_rate,
                row.mean_uncertainty
            )
        end
    end
end

function write_reliability_curve(path::String, rows)
    open(path, "w") do io
        println(io, "day,reliability,cumulative_failure_probability")
        for row in rows
            @printf(
                io,
                "%d,%.6f,%.6f\n",
                row.day,
                row.reliability,
                row.cumulative_failure_probability
            )
        end
    end
end

events = simulate_events(5000; seed = 42, shift = 2.0)
sweep = threshold_sweep(events)
reliability = simulate_reliability_curve(1000)

write_threshold_sweep(joinpath(output_dir, "julia_threshold_sweep.csv"), sweep)
write_reliability_curve(joinpath(output_dir, "julia_reliability_curve.csv"), reliability)

println("Julia AI safety reliability simulation complete.")
println("Wrote julia_threshold_sweep.csv and julia_reliability_curve.csv")
