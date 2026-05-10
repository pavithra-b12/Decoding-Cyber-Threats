import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Load CSV
df = pd.read_csv("data/employee_logs.csv")

def calculate_risk(emp_name):
    row = df[df["employee_name"] == emp_name].iloc[0]

    score = (
        row["failed_logins"] * 2 +
        row["off_hours_access"] * 3 +
        row["usb_insertions"] * 4
    )

    if score <= 5:
        level = "LOW"
    elif score <= 12:
        level = "MEDIUM"
    else:
        level = "HIGH"

    messagebox.showinfo(
        "Employee Risk",
        f"Employee: {emp_name}\nRisk Score: {score}\nRisk Level: {level}"
    )

# UI
root = tk.Tk()
root.title("Employee Risk Analysis")

tk.Label(root, text="Select Employee").pack(pady=5)

emp_combo = ttk.Combobox(root, values=df["employee_name"].tolist())
emp_combo.pack(pady=5)

tk.Button(
    root,
    text="Check Risk",
    command=lambda: calculate_risk(emp_combo.get())
).pack(pady=10)

root.mainloop()
