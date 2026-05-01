/*
AI for Scientific Discovery and Computational Research

C example:
Low-level numerical kernel validation for scientific computation.

Compile:
cc numerical_kernel_validation.c -lm -o numerical_kernel_validation

Run:
./numerical_kernel_validation
*/

#include <math.h>
#include <stdio.h>
#include <stdbool.h>

double scientific_function(double x1, double x2) {
    return 1.8 * sin(M_PI * x1) + 1.2 * cos(M_PI * x2) - 0.4 * x2 * x2;
}

bool is_valid_result(double value) {
    return isfinite(value) && value > -10.0 && value < 10.0;
}

int main(void) {
    double inputs[5][2] = {
        {0.10, 0.20},
        {0.35, 0.80},
        {0.50, 0.50},
        {0.75, 0.10},
        {0.95, 0.90}
    };

    int failures = 0;

    for (int i = 0; i < 5; i++) {
        double value = scientific_function(inputs[i][0], inputs[i][1]);

        printf("case=%d x1=%.3f x2=%.3f value=%.6f\n",
               i + 1,
               inputs[i][0],
               inputs[i][1],
               value);

        if (!is_valid_result(value)) {
            failures++;
        }
    }

    printf("Numerical kernel validation complete. Failures: %d\n", failures);

    return failures == 0 ? 0 : 1;
}
