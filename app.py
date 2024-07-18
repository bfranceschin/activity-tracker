from pynput import keyboard
import tkinter as tk
import datetime
import json
import os
import calendar

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.last_key_press_time = datetime.datetime.now()
        self.work_time = datetime.timedelta()
        self.current_week_total = datetime.timedelta()
        self.last_week_total = datetime.timedelta()
        self.current_week_number = datetime.datetime.now().isocalendar()[1]

        if os.path.isfile('work_intervals.json'):
            with open('work_intervals.json', 'r') as f:
                work_intervals_str = json.load(f)
            self.work_intervals = [{'start': datetime.datetime.fromisoformat(interval['start']), 'end': datetime.datetime.fromisoformat(interval['end'])} for interval in work_intervals_str]
        else:
            self.work_intervals = [{'start': self.last_key_press_time, 'end': self.last_key_press_time}]
        
        for interval in self.work_intervals:
            interval_duration = interval['end'] - interval['start']
            if interval['start'].date() == datetime.datetime.now().date():
                self.work_time += interval_duration
        
        self.update_weekday_labels()
    
    def create_widgets(self):
        self.last_key_press_label = tk.Label(self)
        self.last_key_press_label["text"] = "Last key press: N/A"
        self.last_key_press_label.pack(side="top")

        self.elapsed_time_label = tk.Label(self)
        self.elapsed_time_label["text"] = "Elapsed time: N/A"
        self.elapsed_time_label.pack(side="top")

        self.work_time_label = tk.Label(self)
        self.work_time_label["text"] = "Work time: 0.00 seconds"
        self.work_time_label.pack(side="top")

        self.weekday_labels = []
        for i in range(7):
            weekday_label = tk.Label(self)
            weekday_label["text"] = calendar.day_name[i][:3] + ": 00:00:00"
            weekday_label.pack(side="top")
            self.weekday_labels.append(weekday_label)

        self.current_week_label = tk.Label(self)
        self.current_week_label["text"] = "Current Week: 00:00:00"
        self.current_week_label.pack(side="top")

        self.last_week_label = tk.Label(self)
        self.last_week_label["text"] = "Last Week: 00:00:00"
        self.last_week_label.pack(side="top")

    def update_last_key_press_time(self):
        current_time = datetime.datetime.now()
        current_week = current_time.isocalendar()[1]

        if current_week != self.current_week_number:
            self.last_week_total = self.current_week_total
            self.current_week_total = datetime.timedelta()
            self.current_week_number = current_week
            self.update_weekday_labels()

        if current_time.date() != self.last_key_press_time.date():
            self.work_time = datetime.timedelta()

        elapsed_time = current_time - self.last_key_press_time
        self.last_key_press_time = current_time

        if elapsed_time < datetime.timedelta(minutes=10):
            self.work_time += elapsed_time
            self.current_week_total += elapsed_time
            self.work_intervals[-1]['end'] = current_time

            current_day_of_week = current_time.weekday()
            self.weekday_labels[current_day_of_week]["text"] = calendar.day_name[current_day_of_week][:3] + ": " + self.format_elapsed_time(self.work_time)

            self.current_week_label["text"] = "Current Week: " + self.format_elapsed_time(self.current_week_total)
        else:
            self.work_intervals.append({'start': current_time, 'end': current_time})

        self.last_key_press_label["text"] = "Last key press: " + current_time.strftime('%Y-%m-%d %H:%M:%S')
        self.elapsed_time_label["text"] = "Elapsed time: " + self.format_elapsed_time(elapsed_time)
        self.work_time_label["text"] = "Work time: " + self.format_elapsed_time(self.work_time)

    def format_elapsed_time(self, elapsed_time):
        total_seconds = int(elapsed_time.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)
    
    def save_work_intervals(self):
        # Convert datetime.datetime objects to strings in the ISO 8601 format
        work_intervals_str = [{'start': interval['start'].isoformat(), 'end': interval['end'].isoformat()} for interval in self.work_intervals]
        with open('work_intervals.json', 'w') as f:
            json.dump(work_intervals_str, f)
        # Schedule the next save operation to be performed after 5 minutes
        self.master.after(300000, self.save_work_intervals)
    
    def update_weekday_labels(self):
        current_time = datetime.datetime.now()
        current_week = current_time.isocalendar()[1]
        work_time_per_day = [datetime.timedelta() for _ in range(7)]

        self.current_week_total = datetime.timedelta()
        self.last_week_total = datetime.timedelta()

        for interval in self.work_intervals:
            interval_week = interval['start'].isocalendar()[1]
            interval_day_of_week = interval['start'].weekday()
            interval_duration = interval['end'] - interval['start']

            if interval_week == current_week:
                work_time_per_day[interval_day_of_week] += interval_duration
                self.current_week_total += interval_duration
            elif interval_week == current_week - 1:
                self.last_week_total += interval_duration

        for i in range(7):
            self.weekday_labels[i]["text"] = calendar.day_name[i][:3] + ": " + self.format_elapsed_time(work_time_per_day[i])

        self.current_week_label["text"] = "Current Week: " + self.format_elapsed_time(self.current_week_total)
        self.last_week_label["text"] = "Last Week: " + self.format_elapsed_time(self.last_week_total)        

root = tk.Tk()
app = Application(master=root)

def on_press(key):
    app.update_last_key_press_time()

# Start the listener in a non-blocking manner
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the Tkinter event loop
app.save_work_intervals()  # Start the save operation
app.mainloop()

# If the Tkinter event loop is exited, stop the listener
listener.stop()