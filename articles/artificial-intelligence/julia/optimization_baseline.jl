# Simple Optimization Baseline for AI Systems

using Random
using LinearAlgebra
using Statistics

Random.seed!(42)

function sigmoid(z)
    return 1.0 ./ (1.0 .+ exp.(-z))
end

function binary_cross_entropy(y, p)
    eps = 1e-9
    return -mean(y .* log.(p .+ eps) .+ (1 .- y) .* log.(1 .- p .+ eps))
end

n = 1000
d = 5

X = randn(n, d)
true_beta = [0.8, -1.2, 0.5, 0.3, -0.7]
prob = sigmoid(X * true_beta)
y = Float64.(rand(n) .< prob)

beta = zeros(d)
learning_rate = 0.05
epochs = 500

for epoch in 1:epochs
    p = sigmoid(X * beta)
    gradient = X' * (p - y) / n
    beta -= learning_rate * gradient

    if epoch % 100 == 0
        loss = binary_cross_entropy(y, p)
        println("epoch=", epoch, " loss=", round(loss, digits=4))
    end
end

println("learned coefficients: ", beta)
