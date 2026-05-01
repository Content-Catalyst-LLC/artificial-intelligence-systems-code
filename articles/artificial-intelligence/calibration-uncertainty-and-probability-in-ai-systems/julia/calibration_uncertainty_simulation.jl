# Calibration, Uncertainty, and Probability in AI Systems
# Julia workflow for calibration, entropy, uncertainty, and threshold simulation.
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

function simulate_calibration(; n::Int = 4000, seed::Int = 42)
    Random.seed!(seed)

    feature_a = randn(n)
    feature_b = randn(n)

    true_logit = 0.9 .* feature_a .- 0.6 .* feature_b
    true_probability = sigmoid.(true_logit)

    labels = rand(n) .< true_probability

    model_logit = 1.55 .* true_logit .+ 0.55 .* randn(n)
    predicted_probability = sigmoid.(model_logit)

    entropy = .-(
        predicted_probability .* log.(max.(predicted_probability, 1e-9)) .+
        (1 .- predicted_probability) .* log.(max.(1 .- predicted_probability, 1e-9))
    )

    brier = mean((predicted_probability .- labels).^2)
    accuracy = mean((predicted_probability .>= 0.5) .== labels)

    return predicted_probability, labels, entropy, brier, accuracy
end

predicted_probability, labels, entropy, brier, accuracy = simulate_calibration()

open(joinpath(output_dir, "julia_calibration_simulation.csv"), "w") do io
    println(io, "case_id,predicted_probability,label,entropy,uncertainty_zone")
    for i in eachindex(predicted_probability)
        zone = predicted_probability[i] < 0.30 ? "standard_processing" :
               predicted_probability[i] <= 0.75 ? "human_review" : "urgent_review"

        @printf(
            io,
            "CASE-%05d,%.6f,%d,%.6f,%s\n",
            i,
            predicted_probability[i],
            labels[i] ? 1 : 0,
            entropy[i],
            zone
        )
    end
end

open(joinpath(output_dir, "julia_calibration_summary.csv"), "w") do io
    println(io, "accuracy,brier_score,mean_entropy,human_review_rate,urgent_review_rate")
    human_review_rate = mean((predicted_probability .>= 0.30) .& (predicted_probability .<= 0.75))
    urgent_review_rate = mean(predicted_probability .> 0.75)

    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f\n",
        accuracy,
        brier,
        mean(entropy),
        human_review_rate,
        urgent_review_rate
    )
end

println("Julia calibration simulation complete.")
println("Accuracy: ", round(accuracy, digits = 4))
println("Brier score: ", round(brier, digits = 4))
