import tkinter as tk
import math

# --- Constants ---
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#0A6847"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# --- Session Durations (in minutes) ---
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# --- Global State ---
reps = 0
timer_id = None


# --- Timer Functions ---

def reset_timer():
    """Stops the timer, clears display, and resets session tracking."""
    global reps, timer_id
    if timer_id:
        window.after_cancel(timer_id)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer!", fg=GREEN)
    checkmark_label.config(text="")
    reps = 0

def start_timer():
    """Starts the timer, determining session type."""
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break!", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break!", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="Work!", fg=GREEN)

def count_down(count):
    """Manages countdown logic and display updates."""
    global timer_id

    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        timer_id = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions_done = math.floor(reps / 2)
        for _ in range(work_sessions_done):
            marks += "✔"
        checkmark_label.config(text=marks)


# --- UI Setup ---

window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = tk.Label(
    text="Timer!",
    font=(FONT_NAME, 35, "bold"),
    bg=YELLOW,
    fg=GREEN
)
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
try:
    image_tomato = tk.PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=image_tomato)
except tk.TclError:
    print("Warning: 'tomato.png' not found or is invalid. Displaying only timer text.")
    canvas.create_rectangle(0,0,200,224, fill="lightcoral", outline="lightcoral")


timer_text = canvas.create_text(
    100, 130,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

start_button = tk.Button(text="Start", command=start_timer, highlightbackground=YELLOW)
start_button.grid(column=0, row=2)

reset_button = tk.Button(text="Reset", command=reset_timer, highlightbackground=YELLOW)
reset_button.grid(column=2, row=2)

checkmark_label = tk.Label(
    text="",
    font=(FONT_NAME, 20),
    fg=GREEN,
    bg=YELLOW
)
checkmark_label.grid(column=1, row=3)

window.mainloop()
