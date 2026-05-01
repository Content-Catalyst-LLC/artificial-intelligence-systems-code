# Labor transition sensitivity analysis.
# This workflow estimates how training access affects transition priority.

using Random
using Statistics

Random.seed!(42)

n = 1000
ai_exposure = rand(n)
job_quality = 0.25 .+ 0.60 .* rand(n)

training_values = collect(0.10:0.05:0.95)
results = []

for training_access in training_values
    transition_priority = (ai_exposure .> 0.60) .& (training_access .< 0.50) .& (job_quality .< 0.50)
    push!(results, (training_access, mean(transition_priority)))
end

output_dir = joinpath(@__DIR__, "..", "outputs")
mkpath(output_dir)

open(joinpath(output_dir, "julia_labor_transition_sensitivity.csv"), "w") do io
    println(io, "training_access,transition_priority_rate")
    for row in results
        println(io, "$(row[1]),$(row[2])")
    end
end

println("Labor transition sensitivity analysis complete.")
