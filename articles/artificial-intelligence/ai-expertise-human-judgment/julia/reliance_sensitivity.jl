using Random
using Statistics

Random.seed!(42)

n = 1000
true_risk = rand(n) .^ 2
context_complexity = rand(n)
ai_score = clamp.(true_risk .+ 0.09 .* randn(n), 0, 1)
expert_score = clamp.(true_risk .+ 0.11 .* randn(n), 0, 1)

reliance_values = collect(0.0:0.05:1.0)
results = []

for alpha in reliance_values
    combined = alpha .* ai_score .+ (1 - alpha) .* expert_score
    error = mean(abs.(combined .- true_risk))
    push!(results, (alpha, error))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_reliance_sensitivity.csv"), "w") do io
    println(io, "ai_reliance,mean_absolute_error")
    for row in results
        println(io, "$(row[1]),$(row[2])")
    end
end

println("Reliance sensitivity analysis complete.")
