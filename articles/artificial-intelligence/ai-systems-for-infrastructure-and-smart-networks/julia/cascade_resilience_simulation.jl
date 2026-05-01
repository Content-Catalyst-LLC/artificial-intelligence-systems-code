# AI Systems for Infrastructure and Smart Networks
# Julia workflow for cascade and resilience simulation.
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

function simulate_resilience_curve(; horizon::Int = 120, shock_day::Int = 20, seed::Int = 42)
    Random.seed!(seed)

    performance = ones(Float64, horizon)

    for day in 1:horizon
        if day < shock_day
            performance[day] = 1.0
        else
            damage = 0.55 * exp(-0.045 * (day - shock_day))
            noise = randn() * 0.015
            performance[day] = clamp(1.0 - damage + noise, 0.0, 1.0)
        end
    end

    resilience = mean(performance)

    return performance, resilience
end

function simulate_cascade(n_nodes::Int; seed::Int = 7)
    Random.seed!(seed)

    load = rand(n_nodes) .* 0.6 .+ 0.2
    capacity = load .+ rand(n_nodes) .* 0.4 .+ 0.1

    failed = falses(n_nodes)
    failed[1] = true

    cascade_steps = 0

    while true
        new_failures = falses(n_nodes)

        for i in 1:n_nodes
            if failed[i]
                continue
            end

            neighbor_pressure = sum(failed) / n_nodes
            adjusted_load = load[i] + 0.35 * neighbor_pressure

            if adjusted_load > capacity[i]
                new_failures[i] = true
            end
        end

        if !any(new_failures)
            break
        end

        failed .= failed .| new_failures
        cascade_steps += 1

        if cascade_steps > 50
            break
        end
    end

    return sum(failed), cascade_steps
end

performance, resilience = simulate_resilience_curve()
failed_nodes, cascade_steps = simulate_cascade(100)

open(joinpath(output_dir, "julia_resilience_curve.csv"), "w") do io
    println(io, "day,normalized_performance")
    for i in eachindex(performance)
        @printf(io, "%d,%.6f\n", i, performance[i])
    end
end

open(joinpath(output_dir, "julia_cascade_summary.csv"), "w") do io
    println(io, "failed_nodes,cascade_steps,resilience_index")
    @printf(io, "%d,%d,%.6f\n", failed_nodes, cascade_steps, resilience)
end

println("Julia cascade and resilience simulation complete.")
println("Failed nodes: ", failed_nodes)
println("Cascade steps: ", cascade_steps)
println("Resilience index: ", round(resilience, digits = 4))
