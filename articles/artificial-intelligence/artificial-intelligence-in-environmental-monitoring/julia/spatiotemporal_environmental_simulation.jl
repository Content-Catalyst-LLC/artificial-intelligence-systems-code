# Artificial Intelligence in Environmental Monitoring
# Julia workflow for spatiotemporal environmental simulation and anomaly scoring.
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

function simulate_grid(nx::Int, ny::Int, nt::Int; seed::Int = 42)
    Random.seed!(seed)

    field = zeros(Float64, nx, ny, nt)

    for t in 1:nt
        for i in 1:nx
            for j in 1:ny
                spatial = sin(i / 4.0) + cos(j / 5.0)
                seasonal = 0.4 * sin(t / 8.0)
                trend = 0.006 * t
                noise = randn() * 0.08
                field[i, j, t] = spatial + seasonal + trend + noise
            end
        end
    end

    # Inject an anomaly.
    field[8:12, 8:12, 45:55] .+= 2.0

    return field
end

function anomaly_scores(field)
    nx, ny, nt = size(field)
    scores = zeros(Float64, nx, ny, nt)

    for i in 1:nx
        for j in 1:ny
            series = field[i, j, :]
            mu = mean(series)
            sigma = std(series)
            if sigma == 0
                sigma = 1.0
            end
            scores[i, j, :] = abs.(series .- mu) ./ sigma
        end
    end

    return scores
end

field = simulate_grid(20, 20, 72)
scores = anomaly_scores(field)

open(joinpath(output_dir, "julia_spatiotemporal_anomaly_scores.csv"), "w") do io
    println(io, "x,y,t,value,anomaly_score")
    for i in 1:size(field, 1)
        for j in 1:size(field, 2)
            for t in 1:size(field, 3)
                @printf(io, "%d,%d,%d,%.6f,%.6f\n", i, j, t, field[i, j, t], scores[i, j, t])
            end
        end
    end
end

high_anomaly_share = mean(scores .> 2.5)

open(joinpath(output_dir, "julia_environmental_anomaly_summary.csv"), "w") do io
    println(io, "mean_value,mean_anomaly_score,high_anomaly_share")
    @printf(io, "%.6f,%.6f,%.6f\n", mean(field), mean(scores), high_anomaly_share)
end

println("Julia spatiotemporal environmental simulation complete.")
println("High anomaly share: ", round(high_anomaly_share, digits = 4))
