from typing import List
import matplotlib.pyplot as plt


class Process:
    def __init__(self, pid: str, arrival_time: int, burst_time: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time})"


class FCFS_Scheduler:
    def __init__(self):
        self.processes: List[Process] = []
        self.gantt_chart = []

    def add_process(self, process: Process):
        self.processes.append(process)

    def run(self):
        # Sort by arrival time
        self.processes.sort(key=lambda p: p.arrival_time)
        time = 0
        for p in self.processes:
            if time < p.arrival_time:
                time = p.arrival_time
            p.start_time = time
            time += p.burst_time
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            self.gantt_chart.append((p.pid, p.start_time, p.completion_time))

    def show_results(self):
        print("PID | Arrival | Burst | Start | Completion | Turnaround | Waiting")
        for p in self.processes:
            print(f"{p.pid:>3} | {p.arrival_time:^7} | {p.burst_time:^5} | {p.start_time:^5} | "
                  f"{p.completion_time:^10} | {p.turnaround_time:^10} | {p.waiting_time:^7}")
        avg_tt = sum(p.turnaround_time for p in self.processes) / len(self.processes)
        avg_wt = sum(p.waiting_time for p in self.processes) / len(self.processes)
        print(f"\nAverage Turnaround Time: {avg_tt:.2f}")
        print(f"Average Waiting Time: {avg_wt:.2f}")
        return avg_tt, avg_wt

    def plot_gantt_chart(self):
        fig, ax = plt.subplots()
        for i, (pid, start, end) in enumerate(self.gantt_chart):
            ax.broken_barh([(start, end - start)], (i * 10, 9), facecolors='tab:blue')
            ax.text((start + end) / 2, i * 10 + 4.5, pid, ha='center', va='center', color='white')
        ax.set_ylim(0, len(self.gantt_chart) * 10)
        ax.set_xlim(0, max(end for _, _, end in self.gantt_chart) + 2)
        ax.set_xlabel("Time")
        ax.set_yticks([i * 10 + 4.5 for i in range(len(self.gantt_chart))])
        ax.set_yticklabels([pid for pid, _, _ in self.gantt_chart])
        ax.grid(True)
        plt.title("Gantt Chart - FCFS")
        plt.show()


# Sample use
if __name__ == "__main__":
    scheduler = FCFS_Scheduler()
    scheduler.add_process(Process("P1", 0, 5))
    scheduler.add_process(Process("P2", 2, 3))
    scheduler.add_process(Process("P3", 4, 1))
    scheduler.add_process(Process("P4", 6, 2))
    scheduler.run()
    scheduler.show_results()
    scheduler.plot_gantt_chart()
