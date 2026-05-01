# AI in Education, Knowledge Work, and Learning Systems
# Julia workflow for learning gain and assistance-gap simulation.
#
# Educational systems workflow only.

using Random
using Statistics
using Printf

article_dir = joinpath(@__DIR__, "..")
output_dir = joinpath(article_dir, "outputs")

if !isdir(output_dir)
    mkpath(output_dir)
end

clamp(x; lower = 0.0, upper = 1.0) = min(max(x, lower), upper)

function simulate_learning(; n::Int = 3000, seed::Int = 42)
    Random.seed!(seed)

    baseline = [clamp(randn() * 0.17 + 0.52) for _ in 1:n]
    effort = [clamp(randn() * 0.18 + 0.62) for _ in 1:n]
    ai_use = rand(n)
    teacher_quality = [clamp(randn() * 0.16 + 0.68) for _ in 1:n]

    learning_gain = [
        clamp(0.10 + 0.14 * effort[i] + 0.12 * ai_use[i] * teacher_quality[i] - 0.05 * ai_use[i] * (1 - effort[i]), lower = -1.0, upper = 1.0)
        for i in 1:n
    ]

    post_learning = [clamp(baseline[i] + learning_gain[i]) for i in 1:n]

    assisted = [
        clamp(post_learning[i] + 0.16 * ai_use[i] + randn() * 0.04)
        for i in 1:n
    ]

    independent_transfer = [
        clamp(post_learning[i] + 0.06 * effort[i] - 0.14 * ai_use[i] * (1 - effort[i]) + randn() * 0.05)
        for i in 1:n
    ]

    assistance_gap = assisted .- independent_transfer

    return baseline, effort, ai_use, teacher_quality, learning_gain, assisted, independent_transfer, assistance_gap
end

baseline, effort, ai_use, teacher_quality, learning_gain, assisted, independent_transfer, assistance_gap = simulate_learning()

open(joinpath(output_dir, "julia_learning_gain_assistance_gap.csv"), "w") do io
    println(io, "record_id,baseline,effort,ai_use,teacher_quality,learning_gain,assisted_performance,independent_transfer,assistance_gap")
    for i in eachindex(baseline)
        @printf(
            io,
            "LEARN-%05d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
            i,
            baseline[i],
            effort[i],
            ai_use[i],
            teacher_quality[i],
            learning_gain[i],
            assisted[i],
            independent_transfer[i],
            assistance_gap[i]
        )
    end
end

open(joinpath(output_dir, "julia_learning_summary.csv"), "w") do io
    println(io, "mean_learning_gain,mean_assisted_performance,mean_independent_transfer,mean_assistance_gap")
    @printf(
        io,
        "%.6f,%.6f,%.6f,%.6f\n",
        mean(learning_gain),
        mean(assisted),
        mean(independent_transfer),
        mean(assistance_gap)
    )
end

println("Julia learning gain and assistance-gap simulation complete.")
