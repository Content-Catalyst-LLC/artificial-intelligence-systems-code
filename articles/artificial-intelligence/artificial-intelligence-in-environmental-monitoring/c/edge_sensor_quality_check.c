/*
Artificial Intelligence in Environmental Monitoring

C example:
Embedded-style environmental sensor quality check.

Compile:
cc edge_sensor_quality_check.c -o edge_sensor_quality_check

Run:
./edge_sensor_quality_check
*/

#include <stdio.h>
#include <stdbool.h>

typedef struct {
    const char *sensor_id;
    const char *variable_name;
    double value;
    double min_allowed;
    double max_allowed;
    double sensor_health;
} SensorReading;

bool validate_reading(SensorReading reading) {
    if (reading.value < reading.min_allowed || reading.value > reading.max_allowed) {
        printf("FAIL: %s %s value %.3f outside range %.3f to %.3f\n",
               reading.sensor_id,
               reading.variable_name,
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
        {"air_sensor_001", "pm25", 12.4, 0.0, 500.0, 0.92},
        {"water_sensor_002", "turbidity", 18.2, 0.0, 1000.0, 0.68},
        {"weather_sensor_003", "temperature", 39.1, -80.0, 80.0, 0.88},
        {"eco_sensor_004", "vegetation_index", 1.2, 0.0, 1.0, 0.94}
    };

    int count = sizeof(readings) / sizeof(readings[0]);
    int failed = 0;

    for (int i = 0; i < count; i++) {
        if (!validate_reading(readings[i])) {
            failed++;
        }
    }

    printf("Environmental edge sensor validation complete. Records requiring review: %d\n", failed);

    return failed == 0 ? 0 : 1;
}
