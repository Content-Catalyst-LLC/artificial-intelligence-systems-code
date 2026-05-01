# AI in Health, Medicine, and Clinical Decision Support
# Julia workflow for clinical risk prediction and threshold simulation.
#
# Educational systems workflow only; not medical advice.

using Random
using Statistics
using Printf

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

sigmoid(x) = 1.0 / (1.0 + exp(-x))

function simulate_clinical_thresholds(; n::Int = 4000, seed::Int = 42)
    Random.seed!(seed)

    vital = randn(n)
    labs = randn(n)
    comorbidity = rand(n) .* 3.0

    true_logit = 0.85 .* vital .+ 0.65 .* labs .+ 0.45 .* comorbidity .- 2.2
    true_probability = sigmoid.(true_logit)
    outcomes = rand(n) .< true_probability

    model_logit = 0.75 .* vital .+ 0.55 .* labs .+ 0.35 .* comorbidity .- 2.0 .+ 0.45 .* randn(n)
    predicted_probability = sigmoid.(model_logit)

    return predicted_probability, outcomes
end

function metrics_at_threshold(predicted_probability, outcomes, threshold)
    alerts = predicted_probability .>= threshold

    tp = sum(alerts .& outcomes)
    fp = sum(alerts .& .!outcomes)
    tn = sum(.!alerts .& .!outcomes)
    fn = sum(.!alerts .& outcomes)

    sensitivity = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    alert_rate = mean(alerts)
    false_negative_rate = fn / max(tp + fn, 1)

    utility = (2.0 * tp - 0.25 * fp - 4.0 * fn - 0.05 * sum(alerts)) / length(outcomes)

    return sensitivity, specificity, alert_rate, false_negative_rate, utility
end

predicted_probability, outcomes = simulate_clinical_thresholds()

thresholds = collect(0.10:0.05:0.60)

open(joinpath(output_dir, "julia_clinical_threshold_summary.csv"), "w") do io
    println(io, "threshold,sensitivity,specificity,alert_rate,false_negative_rate,utility")
    for threshold in thresholds
        sensitivity, specificity, alert_rate, false_negative_rate, utility = metrics_at_threshold(
            predicted_probability,
            outcomes,
            threshold
        )

        @printf(
            io,
            "%.2f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            threshold,
            sensitivity,
            specificity,
            alert_rate,
            false_negative_rate,
            utility
        )
    end
end

println("Julia clinical AI threshold simulation complete.")
