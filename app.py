from pynput import keyboard
import tkinter as tk
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.last_key_press_time = time.time()  # Initialize the last key press time
        self.work_time = 0  # Initialize work time

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
        current_time = time.time()
        elapsed_time = current_time - self.last_key_press_time
        self.last_key_press_time = current_time  # Update the last key press time

        # If elapsed time is less than 10 minutes (600 seconds), add it to work time
        if elapsed_time < 600:
            self.work_time += elapsed_time

        self.last_key_press_label["text"] = "Last key press: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
        self.elapsed_time_label["text"] = "Elapsed time: " + self.format_time(elapsed_time)
        self.work_time_label["text"] = "Work time: " + self.format_time(self.work_time)

    def format_time(self, time_in_seconds):
        hours = int(time_in_seconds // 3600)
        time_in_seconds %= 3600
        minutes = int(time_in_seconds // 60)
        time_in_seconds %= 60
        seconds = int(time_in_seconds)
        return "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)

root = tk.Tk()
app = Application(master=root)

def on_press(key):
    app.update_last_key_press_time()

# Start the listener in a non-blocking manner
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the Tkinter event loop
app.mainloop()

# If the Tkinter event loop is exited, stop the listener
listener.stop()