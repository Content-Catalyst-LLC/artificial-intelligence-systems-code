# Large Language Models and Foundation Model Systems
# Julia workflow for token-cost, latency, and system-risk simulation.
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

function simulate_llm_operations(; n::Int = 200, seed::Int = 42)
    Random.seed!(seed)

    input_tokens = rand(400:9000, n)
    output_tokens = rand(100:1800, n)
    tool_calls = rand(0:4, n)

    total_tokens = input_tokens .+ output_tokens
    latency_seconds = 0.8 .+ 0.00035 .* total_tokens .+ 0.35 .* tool_calls .+ rand(n)

    grounding_score = rand(n) .* 0.45 .+ 0.50
    safety_score = rand(n) .* 0.35 .+ 0.60

    system_risk = clamp.(
        0.30 .* (1 .- grounding_score) .+
        0.25 .* (1 .- safety_score) .+
        0.20 .* (total_tokens ./ 11000) .+
        0.15 .* (latency_seconds ./ 10) .+
        0.10 .* (tool_calls ./ 4),
        0.0,
        1.0
    )

    return input_tokens, output_tokens, tool_calls, total_tokens, latency_seconds, grounding_score, safety_score, system_risk
end

input_tokens, output_tokens, tool_calls, total_tokens, latency_seconds, grounding_score, safety_score, system_risk = simulate_llm_operations()

open(joinpath(output_dir, "julia_llm_cost_latency_simulation.csv"), "w") do io
    println(io, "case_id,input_tokens,output_tokens,tool_calls,total_tokens,latency_seconds,grounding_score,safety_score,system_risk")
    for i in eachindex(total_tokens)
        @printf(
            io,
            "CASE-%03d,%d,%d,%d,%d,%.6f,%.6f,%.6f,%.6f\n",
            i,
            input_tokens[i],
            output_tokens[i],
            tool_calls[i],
            total_tokens[i],
            latency_seconds[i],
            grounding_score[i],
            safety_score[i],
            system_risk[i]
        )
    end
end

open(joinpath(output_dir, "julia_llm_system_summary.csv"), "w") do io
    println(io, "mean_total_tokens,mean_latency_seconds,mean_grounding_score,mean_safety_score,mean_system_risk,high_risk_cases")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f,%.6f,%d\n",
        mean(total_tokens),
        mean(latency_seconds),
        mean(grounding_score),
        mean(safety_score),
        mean(system_risk),
        sum(system_risk .> 0.45)
    )
end

println("Julia LLM cost-latency simulation complete.")
println("Mean system risk: ", round(mean(system_risk), digits = 4))
