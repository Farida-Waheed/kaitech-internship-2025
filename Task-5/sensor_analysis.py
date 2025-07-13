import pandas as pd
import json
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


# Group data by sensor
sensor_dict = defaultdict(list)
for entry in sensor_data:
    sensor_id, *data = entry
    sensor_dict[sensor_id].append(tuple(data))

# Unique sensors with stress > 13.0
high_stress_sensors = {sid for sid, _, _, stress, _ in sensor_data if stress > 13.0}

# Stats per sensor
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

# Sorted timestamps
timestamps = sorted({entry[1] for entry in sensor_data})

# Most recent readings
latest_readings = {}
for entry in sensor_data:
    sid, ts, *rest = entry
    if sid not in latest_readings or ts > latest_readings[sid][0]:
        latest_readings[sid] = (ts, *rest)
most_recent_tuple = tuple(latest_readings.values())

# Print Outputs
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


# Convert to DataFrame
df = pd.DataFrame(sensor_data, columns=["Sensor", "Timestamp", "Temperature", "Stress", "Displacement"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# 1. Organized readings per sensor
organized = df.sort_values(by=["Sensor", "Timestamp"])
organized.to_json("1_organized_readings.json", orient="records", indent=4)

# 2. Unique sensors with extreme values (Temp > mean OR Stress > 13)
extreme_df = df[(df["Temperature"] > df["Temperature"].mean()) | (df["Stress"] > 13.0)]
extreme_df.to_json("2_extreme_sensors.json", orient="records", indent=4)

# 3. Comparison by hour
df["Hour"] = df["Timestamp"].dt.hour
comparison = df.pivot_table(index="Sensor", columns="Hour", values="Temperature")
comparison.to_json("3_comparison_by_hour.json", orient="index", indent=4)

# 4. Summary stats
summary = df.groupby("Sensor").agg({
    "Temperature": ["max", "min", "mean"],
    "Stress": ["max", "min", "mean"],
    "Displacement": ["max", "min", "mean"]
})
summary.columns = ['_'.join(col).strip() for col in summary.columns]
summary.reset_index(inplace=True)
summary.to_json("4_summary_stats.json", orient="records", indent=4)

# 5. Group data by sensor using dict
grouped_dict = defaultdict(list)
for sensor_id, timestamp, temp, stress, disp in sensor_data:
    grouped_dict[sensor_id].append((timestamp, temp, stress, disp))
with open("5_grouped_by_sensor.json", "w") as f:
    json.dump(grouped_dict, f, indent=4)

# 6. Unique sensors with stress > 13.0
stress_sensors = set(df[df["Stress"] > 13.0]["Sensor"])
with open("6_stress_sensors.json", "w") as f:
    json.dump(list(stress_sensors), f, indent=4)

# 7. Statistics per sensor
stats_dict = {}
for sensor in df["Sensor"].unique():
    temp_values = df[df["Sensor"] == sensor]["Temperature"]
    disp_values = df[df["Sensor"] == sensor]["Displacement"]
    stats_dict[sensor] = {
        "Temperature": {
            "Max": temp_values.max(),
            "Min": temp_values.min(),
            "Avg": temp_values.mean()
        },
        "Displacement": {
            "Max": disp_values.max()
        }
    }
with open("7_sensor_stats.json", "w") as f:
    json.dump(stats_dict, f, indent=4)

# 8. Temperature stats per sensor
temp_stats = df.groupby("Sensor")["Temperature"].agg(["max", "min", "mean"]).reset_index()
temp_stats.to_json("8_temperature_stats.json", orient="records", indent=4)

# 9. Max displacement
disp_stats = df.groupby("Sensor")["Displacement"].max().reset_index()
disp_stats.to_json("9_max_displacement.json", orient="records", indent=4)

# 10. Sorted timestamps list
timestamps_str = sorted(df["Timestamp"].dt.strftime('%Y-%m-%d %H:%M').tolist())
with open("10_sorted_timestamps.json", "w") as f:
    json.dump(timestamps_str, f, indent=4)

# 11. Most recent reading per sensor
recent_dict = {}
for sensor in df["Sensor"].unique():
    latest_row = df[df["Sensor"] == sensor].sort_values(by="Timestamp", ascending=False).iloc[0]
    recent_dict[sensor] = tuple(str(x) for x in latest_row.values)
with open("11_most_recent_readings.json", "w") as f:
    json.dump(recent_dict, f, indent=4)


with pd.ExcelWriter("sensor_data_summary.xlsx", engine="openpyxl") as writer:
    organized.to_excel(writer, sheet_name="1_Organized", index=False)
    extreme_df.to_excel(writer, sheet_name="2_Extremes", index=False)
    comparison.to_excel(writer, sheet_name="3_Comparison")
    summary.to_excel(writer, sheet_name="4_Summary", index=False)
    pd.DataFrame(
        [(sensor, *vals) for sensor, readings in grouped_dict.items() for vals in readings],
        columns=["Sensor", "Timestamp", "Temperature", "Stress", "Displacement"]
    ).to_excel(writer, sheet_name="5_Grouped", index=False)
    pd.DataFrame({"Stress_Sensors": list(stress_sensors)}).to_excel(writer, sheet_name="6_Stress_Sensors", index=False)
    pd.DataFrame([
        {
            "Sensor": sensor,
            "Temp_Max": stats["Temperature"]["Max"],
            "Temp_Min": stats["Temperature"]["Min"],
            "Temp_Avg": stats["Temperature"]["Avg"],
            "Disp_Max": stats["Displacement"]["Max"]
        }
        for sensor, stats in stats_dict.items()
    ]).to_excel(writer, sheet_name="7_Sensor_Stats", index=False)
    temp_stats.to_excel(writer, sheet_name="8_Temp_Stats", index=False)
    disp_stats.to_excel(writer, sheet_name="9_Max_Disp", index=False)
    pd.DataFrame({"Timestamps": timestamps_str}).to_excel(writer, sheet_name="10_Timestamps", index=False)
    pd.DataFrame.from_dict(recent_dict, orient="index", columns=df.columns).to_excel(writer, sheet_name="11_Recent", index=True)

print("Done! Excel and JSON files are created successfully.")
