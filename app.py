from pynput import keyboard
import tkinter as tk
import datetime
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.last_key_press_time = datetime.datetime.now()  # Initialize the last key press time
        self.work_time = datetime.timedelta()  # Initialize work time
        self.work_intervals = [{'start': self.last_key_press_time, 'end': self.last_key_press_time}]  # Initialize work intervals

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

    def update_last_key_press_time(self):
        current_time = datetime.datetime.now()
        elapsed_time = current_time - self.last_key_press_time
        self.last_key_press_time = current_time  # Update the last key press time

        # If elapsed time is less than 10 minutes, update the end of the current interval
        if elapsed_time < datetime.timedelta(minutes=10):
            self.work_time += elapsed_time
            self.work_intervals[-1]['end'] = current_time  # Update the end of the current interval
        else:
            # If elapsed time is greater than 10 minutes, start a new interval and make it the current interval
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