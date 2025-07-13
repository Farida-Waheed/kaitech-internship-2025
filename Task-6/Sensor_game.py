import tkinter as tk
from tkinter import ttk
from collections import defaultdict
from datetime import datetime

# Sensor data
sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]

# Convert timestamps
for i in range(len(sensor_data)):
    sid, ts, temp, stress, disp = sensor_data[i]
    sensor_data[i] = (sid, datetime.strptime(ts, "%Y-%m-%d %H:%M"), temp, stress, disp)

class SensorAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💾 SENSOR ANALYZER 3000")
        self.root.configure(bg="#f8cfd5")  # Light soft pink
        self.root.geometry("800x650")
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
    background="#f3a6b2",  # warmer pink
    foreground="#590d82",  # rich purple text
    font=("Courier New", 10, "bold"),
    padding=6
)
        style.configure("TLabel",
                        background="#fde2e4",
                        foreground="#4b0082",
                        font=("Courier New", 12, "bold"))

        # Title frame
        title_frame = tk.Frame(self.root, bg="#fcd5ce", bd=2, relief="ridge")  # warm blush tone
        title_frame.pack(pady=5, fill="x")
        title_label = tk.Label(title_frame, text="""
 ____  ____  _   _ ____  ____   ___  ____  ____  
|  _ \|  _ \| | | |  _ \|  _ \ / _ \|  _ \|  _ \ 
| | | | |_) | | | | |_) | | | | | | | |_) | | | |
| |_| |  _ <| |_| |  __/| |_| | |_| |  _ <| |_| |
|____/|_| \_\\\\___/|_|   |____/ \___/|_| \_\\____/ 
        """, fg="#800080", bg="#fcd5ce", font=("Courier New", 10, "bold"), justify="center")
        title_label.pack()

        # Button panel
        button_frame = tk.LabelFrame(self.root, text=" 🛠 Controls ", fg="#800080", bg="#f8cfd5", font=("Courier New", 12, "bold"), bd=2)
        button_frame.pack(pady=10, padx=10, fill="x")

        actions = [
            ("📦 Organize Readings", self.organize_readings),
            ("🚨 Identify Extremes", self.identify_extreme),
            ("⏱ Compare Intervals", self.compare_intervals),
            ("📊 Sensor Summary", self.summarize_data),
            ("🔥 High Stress > 13", self.high_stress_sensors),
            ("📅 Sort Timestamps", self.sort_timestamps),
            ("🕵️‍♂️ Latest Readings", self.most_recent_readings)
        ]

        for text, command in actions:
            ttk.Button(button_frame, text=text, command=command).pack(pady=3, padx=10, fill="x")

        # Output terminal
        output_frame = tk.LabelFrame(self.root, text=" 🧾 Terminal Output ", fg="#800080", bg="#fde2e4", font=("Courier New", 12, "bold"), bd=2)
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.result_box = tk.Text(
    output_frame, width=90, height=20,
    bg="#ffeaf4",  # VS Code output match (light lavender-pink)
    fg="#800080", insertbackground="#800080",
    font=("Courier New", 10), bd=5, relief="sunken"
)

        self.result_box.pack(padx=10, pady=10, fill="both", expand=True)

    def display(self, data):
        self.result_box.delete("1.0", tk.END)
        if isinstance(data, (list, set)):
            for item in data:
                self.result_box.insert(tk.END, str(item) + "\n")
        elif isinstance(data, dict):
            for k, v in data.items():
                self.result_box.insert(tk.END, f"{k}: {v}\n")
        else:
            self.result_box.insert(tk.END, str(data) + "\n")

    def organize_readings(self):
        sensor_dict = defaultdict(list)
        for sid, ts, temp, stress, disp in sensor_data:
            sensor_dict[sid].append((ts, temp, stress, disp))
        self.display(sensor_dict)

    def identify_extreme(self):
        extreme_sensors = {
            sid for sid, _, temp, stress, _ in sensor_data
            if temp > 36.5 or stress > 13.5
        }
        self.display(f"🚨 Extreme Sensors: {extreme_sensors}")

    def compare_intervals(self):
        interval_map = defaultdict(list)
        for sid, ts, temp, stress, disp in sensor_data:
            hour = ts.hour
            interval_map[(sid, hour)].append((temp, stress, disp))
        self.display(interval_map)

    def summarize_data(self):
        sensor_summary = {}
        for sid in set([x[0] for x in sensor_data]):
            readings = [(t, s, d) for s_id, _, t, s, d in sensor_data if s_id == sid]
            temps = [x[0] for x in readings]
            disps = [x[2] for x in readings]
            sensor_summary[sid] = {
                "Max Temp": max(temps),
                "Min Temp": min(temps),
                "Avg Temp": round(sum(temps) / len(temps), 2),
                "Max Displacement": max(disps)
            }
        self.display(sensor_summary)

    def high_stress_sensors(self):
        stress_set = {sid for sid, _, _, stress, _ in sensor_data if stress > 13.0}
        self.display(f"🔥 Sensors with stress > 13.0: {stress_set}")

    def sort_timestamps(self):
        timestamps = sorted([ts for _, ts, _, _, _ in sensor_data])
        self.display([ts.strftime('%Y-%m-%d %H:%M') for ts in timestamps])

    def most_recent_readings(self):
        recent = {}
        for sid, ts, temp, stress, disp in sensor_data:
            if sid not in recent or ts > recent[sid][0]:
                recent[sid] = (ts, temp, stress, disp)
        self.display(recent)

if __name__ == '__main__':
    root = tk.Tk()
    app = SensorAnalyzerApp(root)
    root.mainloop()
