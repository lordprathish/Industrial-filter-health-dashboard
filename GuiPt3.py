import tkinter as tk
from tkinter import ttk
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# -----------------------------
# Dashboard Configuration
# -----------------------------
NORMAL_COLOR = "#4CAF50"
WARNING_COLOR = "#FFD600"
DANGER_COLOR = "#FF3D00"
BG_COLOR = "#F5F5F5"
TITLE_COLOR = "#1A237E"

TEMP_LIMITS = (0, 60, 80)
PRESS_LIMITS = (0, 90, 120)
HUMID_LIMITS = (0, 60, 80)
GAS_LIMIT = 300

# Units for each parameter
UNITS = {
    "Temperature": "°C",
    "Pressure": "kPa",
    "Humidity": "% RH",
    "Gas": "ppm"
}

# -----------------------------
# Create Main Window
# -----------------------------
root = tk.Tk()
root.title("Industrial Filter Health Dashboard")
root.geometry("1400x800")
root.configure(bg=BG_COLOR)

# -----------------------------
# Title Section
# -----------------------------
title = tk.Label(root, text="Industrial Filter Health Dashboard",
                 font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TITLE_COLOR)
title.pack(pady=10)

timestamp_label = tk.Label(root, text="Last updated: --:--:--",
                           font=("Arial", 12), bg=BG_COLOR)
timestamp_label.pack()

# -----------------------------
# Layout Frames
# -----------------------------
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

left_panel = tk.Frame(main_frame, bg=BG_COLOR)
left_panel.pack(side="left", fill="both", expand=True)

right_panel = tk.Frame(main_frame, bg=BG_COLOR, width=300)
right_panel.pack(side="right", fill="y", padx=10)

# -----------------------------
# Indicator Section
# -----------------------------
indicator_frame = tk.LabelFrame(left_panel, text="Sensor Indicators", font=("Arial", 14, "bold"),
                                bg="white", fg=TITLE_COLOR, padx=10, pady=10)
indicator_frame.pack(side="top", anchor="nw", padx=10, pady=10)

def create_gauge(parent, title):
    frame = tk.Frame(parent, bg="white", bd=2, relief="groove")
    frame.pack(side="left", padx=15, pady=10)

    label_title = tk.Label(frame, text=title, font=("Arial", 12, "bold"), bg="white")
    label_title.pack(pady=8)

    canvas = tk.Canvas(frame, width=130, height=130, bg="white", highlightthickness=0)
    canvas.pack()

    value_label = tk.Label(frame, text="--", font=("Arial", 14, "bold"), bg="white")
    value_label.pack(pady=4)

    return canvas, value_label

temp_canvas, temp_label = create_gauge(indicator_frame, "Temperature (°C)")
press_canvas, press_label = create_gauge(indicator_frame, "Pressure (kPa)")
humid_canvas, humid_label = create_gauge(indicator_frame, "Humidity (%)")
gas_canvas, gas_label = create_gauge(indicator_frame, "Gas (ppm)")

# -----------------------------
# Black Status Window inside Indicator Section
# -----------------------------
status_window = tk.LabelFrame(indicator_frame, text="Status Window",
                              font=("Arial", 12, "bold"), bg="black", fg="white", padx=5, pady=5)
status_window.pack(side="bottom", fill="x", padx=10, pady=10)

status_textbox = tk.Text(status_window, height=6, bg="black", fg="yellow",
                         font=("Consolas", 11), wrap="word")
status_textbox.pack(fill="both", expand=True)
status_textbox.insert("end", "System Initialized...\n")
status_textbox.configure(state="disabled")

# -----------------------------
# Graph Area (Tabbed)
# -----------------------------
notebook = ttk.Notebook(left_panel)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

graphs = {}
parameters = ["Temperature", "Pressure", "Humidity"]

for param in parameters:
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=param)
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title(f"{param} Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(f"{param} ({UNITS[param]})")
    ax.grid(True)
    graphs[param] = {"frame": frame, "figure": fig, "ax": ax,
                     "data": [], "canvas": FigureCanvasTkAgg(fig, master=frame)}
    graphs[param]["canvas"].draw()
    graphs[param]["canvas"].get_tk_widget().pack(fill="both", expand=True)

# -----------------------------
# Right Panel for System Summary
# -----------------------------
status_title = tk.Label(right_panel, text="System Summary",
                        font=("Arial", 16, "bold"), bg=BG_COLOR, fg=TITLE_COLOR)
status_title.pack(pady=20)

status_text = tk.Label(right_panel, text="All systems normal",
                       font=("Arial", 14), bg=BG_COLOR, fg=NORMAL_COLOR, wraplength=250, justify="left")
status_text.pack(pady=10)

# -----------------------------
# Utility Functions
# -----------------------------
def draw_gauge(canvas, value, limits, color):
    canvas.delete("all")
    canvas.create_oval(10, 10, 120, 120, outline="#ddd", width=12)
    angle = min(max(value / limits[2] * 180, 0), 180)
    canvas.create_arc(10, 10, 120, 120, start=180, extent=-angle,
                      style="arc", outline=color, width=12)

def get_color(value, limits):
    if value < limits[1]:
        return NORMAL_COLOR
    elif value < limits[2]:
        return WARNING_COLOR
    else:
        return DANGER_COLOR

def log_status(message, color):
    """Write a message in the black status window."""
    status_textbox.configure(state="normal")
    status_textbox.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n", ("color",))
    status_textbox.tag_config("color", foreground=color)
    status_textbox.see("end")
    status_textbox.configure(state="disabled")

def update_dashboard():
    # Simulated sensor data
    temp = random.uniform(20, 100)
    press = random.uniform(60, 140)
    humid = random.uniform(30, 90)
    gas = random.uniform(100, 500)

    timestamp_label.config(text=f"Last updated: {time.strftime('%H:%M:%S')}")

    # Update Gauges
    for (name, val, canvas, label, limits) in [
        ("Temperature", temp, temp_canvas, temp_label, TEMP_LIMITS),
        ("Pressure", press, press_canvas, press_label, PRESS_LIMITS),
        ("Humidity", humid, humid_canvas, humid_label, HUMID_LIMITS)
    ]:
        color = get_color(val, limits)
        draw_gauge(canvas, val, limits, color)
        label.config(text=f"{val:.1f} {UNITS[name]}", fg=color)

    gas_color = get_color(gas, (0, GAS_LIMIT, GAS_LIMIT + 100))
    draw_gauge(gas_canvas, gas, (0, GAS_LIMIT, GAS_LIMIT + 100), gas_color)
    gas_label.config(text=f"{gas:.1f} {UNITS['Gas']}", fg=gas_color)

    # Update Graphs
    for param, val in [("Temperature", temp), ("Pressure", press), ("Humidity", humid)]:
        g = graphs[param]
        g["data"].append(val)
        if len(g["data"]) > 20:
            g["data"].pop(0)
        g["ax"].clear()
        g["ax"].plot(g["data"], marker="o")
        g["ax"].set_title(f"{param} Over Time")
        g["ax"].set_ylabel(f"{param} ({UNITS[param]})")
        g["ax"].grid(True)
        g["canvas"].draw()

    # Alerts and Colors
    alerts = []
    if temp > TEMP_LIMITS[2]:
        alerts.append(("High Temperature detected!", DANGER_COLOR))
    elif temp > TEMP_LIMITS[1]:
        alerts.append(("Temperature Warning", WARNING_COLOR))

    if press > PRESS_LIMITS[2]:
        alerts.append(("High Pressure detected!", DANGER_COLOR))
    elif press > PRESS_LIMITS[1]:
        alerts.append(("Pressure Warning", WARNING_COLOR))

    if humid > HUMID_LIMITS[2]:
        alerts.append(("High Humidity detected!", DANGER_COLOR))
    elif humid > HUMID_LIMITS[1]:
        alerts.append(("Humidity Warning", WARNING_COLOR))

    if gas > GAS_LIMIT:
        alerts.append(("Harmful Gas Level detected!", DANGER_COLOR))
    elif gas > GAS_LIMIT - 50:
        alerts.append(("Gas Level Warning", WARNING_COLOR))

    # Display Alerts
    if alerts:
        latest_message, color = alerts[-1]
        status_text.config(text=latest_message, fg=color)
        log_status(latest_message, color)
    else:
        status_text.config(text="All systems normal", fg=NORMAL_COLOR)
        log_status("All systems normal", NORMAL_COLOR)

    root.after(2000, update_dashboard)

# -----------------------------
# Run Dashboard
# -----------------------------
update_dashboard()
root.mainloop()
