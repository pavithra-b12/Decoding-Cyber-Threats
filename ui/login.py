import tkinter as tk
from tkinter import messagebox
from utils.auth import authenticate_user, init_db
from ui.dashboard import dashboard_window

# 🔥 ADD THESE IMPORTS
from utils.risk import process_and_send_risk_report
from utils.session import session


def login_window():
    init_db()

    root = tk.Tk()
    root.title("Cyber Threat Monitoring System - Login")
    root.geometry("500x420")
    root.configure(bg="#f4f6f8")
    root.resizable(False, False)

    # ================= HEADER =================
    header = tk.Frame(root, bg="#1f2933", height=80)
    header.pack(fill="x")

    tk.Label(
        header,
        text="CYBER THREAT SECURITY",
        bg="#1f2933",
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=22)

    # ================= LOGIN CARD =================
    card = tk.Frame(root, bg="white", bd=1, relief="solid")
    card.pack(pady=35, ipadx=20, ipady=15)

    tk.Label(
        card,
        text="Login",
        font=("Segoe UI", 16, "bold"),
        bg="white"
    ).pack(pady=10)

    # ================= USERNAME =================
    tk.Label(
        card,
        text="Username",
        font=("Segoe UI", 11),
        bg="white"
    ).pack(anchor="w", padx=10, pady=(10, 2))

    username_entry = tk.Entry(card, width=28, font=("Segoe UI", 11))
    username_entry.pack(padx=10)

    # ================= PASSWORD =================
    tk.Label(
        card,
        text="Password",
        font=("Segoe UI", 11),
        bg="white"
    ).pack(anchor="w", padx=10, pady=(10, 2))

    password_entry = tk.Entry(card, width=28, show="*", font=("Segoe UI", 11))
    password_entry.pack(padx=10)

    # ================= LOGIN FUNCTION =================
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        user = authenticate_user(username, password)

        if user:
            username, role = user
            messagebox.showinfo("Login Successful", f"Welcome {username}")

            # 🔥 SEND RISK MAIL ONLY ONCE PER LOGIN
            if not session["risk_mail_sent"]:
                print("📧 Sending consolidated risk report email...")
                result = process_and_send_risk_report()
                print(result)
                session["risk_mail_sent"] = True

            root.destroy()
            dashboard_window(username, role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # ================= LOGIN BUTTON =================
    login_btn = tk.Button(
        root,
        text="LOGIN",
        width=30,
        height=2,
        bg="#2563eb",
        fg="white",
        font=("Segoe UI", 12, "bold"),
        relief="raised",
        bd=2,
        cursor="hand2",
        command=handle_login
    )
    login_btn.pack(pady=15)

    root.mainloop()


# ================= APP START =================
if __name__ == "__main__":
    login_window()