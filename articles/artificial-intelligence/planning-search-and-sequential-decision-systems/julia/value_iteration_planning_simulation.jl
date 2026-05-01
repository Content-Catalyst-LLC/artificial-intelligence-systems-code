# Planning, Search, and Sequential Decision Systems
# Julia workflow for value iteration and sequential decision risk simulation.
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

function value_iteration(; n_states::Int = 8, n_actions::Int = 3, gamma::Float64 = 0.92, iterations::Int = 80, seed::Int = 42)
    Random.seed!(seed)

    rewards = randn(n_states, n_actions) .* 0.2
    rewards[n_states, :] .= 1.0

    transitions = Array{Float64}(undef, n_states, n_actions, n_states)

    for s in 1:n_states
        for a in 1:n_actions
            raw = rand(n_states)
            raw[s] += 1.0
            transitions[s, a, :] = raw ./ sum(raw)
        end
    end

    values = zeros(n_states)

    for _ in 1:iterations
        new_values = similar(values)

        for s in 1:n_states
            action_values = zeros(n_actions)

            for a in 1:n_actions
                action_values[a] = rewards[s, a] + gamma * sum(transitions[s, a, :] .* values)
            end

            new_values[s] = maximum(action_values)
        end

        values = new_values
    end

    policy = zeros(Int, n_states)

    for s in 1:n_states
        action_values = zeros(n_actions)

        for a in 1:n_actions
            action_values[a] = rewards[s, a] + gamma * sum(transitions[s, a, :] .* values)
        end

        policy[s] = argmax(action_values)
    end

    return rewards, transitions, values, policy
end

rewards, transitions, values, policy = value_iteration()

planning_records = [
    (state = s, selected_action = policy[s], value = values[s], reward = rewards[s, policy[s]])
    for s in eachindex(policy)
]

open(joinpath(output_dir, "julia_value_iteration_policy.csv"), "w") do io
    println(io, "state,selected_action,value,reward")
    for row in planning_records
        @printf(io, "%d,%d,%.6f,%.6f\n", row.state, row.selected_action, row.value, row.reward)
    end
end

open(joinpath(output_dir, "julia_value_iteration_summary.csv"), "w") do io
    println(io, "mean_value,max_value,min_value,unique_actions")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%d\n",
        mean(values),
        maximum(values),
        minimum(values),
        length(unique(policy))
    )
end

println("Julia value iteration workflow complete.")
println("Mean value: ", round(mean(values), digits = 4))
