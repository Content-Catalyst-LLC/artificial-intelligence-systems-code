/*
AI Systems for Infrastructure and Smart Networks

C example:
Embedded-style sensor validation for smart infrastructure telemetry.

Compile:
cc embedded_sensor_validation.c -o embedded_sensor_validation

Run:
./embedded_sensor_validation
*/

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    const char *sensor_id;
    double value;
    double min_allowed;
    double max_allowed;
    double sensor_health;
} SensorReading;

bool validate_reading(SensorReading reading) {
    if (reading.value < reading.min_allowed || reading.value > reading.max_allowed) {
        printf("FAIL: %s value %.3f outside range %.3f to %.3f\n",
               reading.sensor_id,
               reading.value,
               reading.min_allowed,
               reading.max_allowed);
        return false;
    }

    if (reading.sensor_health < 0.70) {
        printf("WARN: %s low sensor health %.3f\n",
               reading.sensor_id,
               reading.sensor_health);
        return false;
    }

    return true;
}

int main(void) {
    SensorReading readings[] = {
        {"pressure_sensor_001", 0.22, 0.00, 1.00, 0.91},
        {"pressure_sensor_002", 1.18, 0.00, 1.00, 0.88},
        {"vibration_sensor_003", 0.31, 0.00, 1.00, 0.66},
        {"flow_sensor_004", 0.72, 0.00, 1.00, 0.94}
    };

    int count = sizeof(readings) / sizeof(readings[0]);
    int failed = 0;

    for (int i = 0; i < count; i++) {
        if (!validate_reading(readings[i])) {
            failed++;
        }
    }

    printf("Sensor validation complete. Records requiring review: %d\n", failed);

    return failed == 0 ? 0 : 1;
}
