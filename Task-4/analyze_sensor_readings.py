from collections import defaultdict
import pprint

# Step 1: Sensor Data
sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]

# Step 2: Organize readings per sensor using dictionary
sensor_dict = defaultdict(list)
for entry in sensor_data:
    sensor_id, *data = entry
    sensor_dict[sensor_id].append(tuple(data))

# Step 3: Find unique sensors with stress > 13.0 using sets
high_stress_sensors = {sid for sid, _, _, stress, _ in sensor_data if stress > 13.0}

# Step 4: Calculate statistics per sensor
sensor_stats = {}
for sid, readings in sensor_dict.items():
    temps = [r[1] for r in readings]
    disps = [r[3] for r in readings]
    sensor_stats[sid] = {
        "max_temp": max(temps),
        "min_temp": min(temps),
        "avg_temp": round(sum(temps) / len(temps), 2),
        "max_displacement": max(disps)
    }

# Step 5: Extract and sort all timestamps into a list
timestamps = sorted({entry[1] for entry in sensor_data})

# Step 6: Most recent reading per sensor as tuple
latest_readings = {}
for entry in sensor_data:
    sid, ts, *rest = entry
    if sid not in latest_readings or ts > latest_readings[sid][0]:
        latest_readings[sid] = (ts, *rest)

most_recent_tuple = tuple(latest_readings.values())

# Output Section
print("Grouped Sensor Data:")
pprint.pprint(dict(sensor_dict))

print("\nSensors with Stress > 13.0:")
print(high_stress_sensors)

print("\nStatistics per Sensor:")
pprint.pprint(sensor_stats)

print("\nSorted Timestamps:")
print(timestamps)

print("\nMost Recent Reading per Sensor (as Tuple):")
pprint.pprint(most_recent_tuple)
