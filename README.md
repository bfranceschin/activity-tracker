# Activity Tracker

User Activity Tracker is a simple Windows application that tracks and displays the time elapsed between keystrokes and the total "work time" (the total time during which the user is active, defined as the time between keystrokes less than 10 minutes).

## Features

- Monitors and displays the time of the last key press.
- Monitors and displays the elapsed time between the last two key strokes.
- Tracks and displays "work time", defined as the time during which the user is considered active. The user is considered active when the time elapsed between two key strokes is less than 10 minutes. The work time is accumulated over these active periods.

## Usage

Run the script with a Python interpreter:

```bash
python app.py
```

Press keys to simulate user activity and watch the GUI update with the relevant times.

Stop the application by closing the GUI window or pressing the Esc key.

## Dependencies
- Python 3.5+
- Tkinter (should be included in the standard Python distribution)
- pynput (pip install pynput)

## Credits
This project was mainly developed with the guidance and assistance of OpenAI's GPT-4

## License
This project is licensed under the terms of the MIT license.
