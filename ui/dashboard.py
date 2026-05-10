import tkinter as tk
from tkinter import messagebox
from utils.risk import get_risky_employees, calculate_risk
from utils.session import session
from tkinter import ttk
import os

def open_visual_dashboard():
    try:
        dashboard_path = r"D:\Desktop\CyberThreatSecurityApp\Cyber_Threat_Dashboard.pbix"
        os.startfile(dashboard_path)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to open Power BI dashboard: {e}")

def dashboard_window(username, role):
    dash = tk.Tk()
    dash.title("Cyber Threat Monitoring Dashboard")
    dash.geometry("1100x650")
    dash.configure(bg="#f4f6f8")

    # ================= LOGOUT =================
    def logout():
        session["risk_mail_sent"] = False
        dash.destroy()

    # ================= HEADER =================
    header = tk.Frame(dash, bg="#1f2933", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="CYBER THREAT MONITORING SYSTEM",
        bg="#1f2933",
        fg="white",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=15)

    # ================= BODY =================
    body = tk.Frame(dash, bg="#f4f6f8")
    body.pack(fill="both", expand=True)

    # ================= MENU =================
    menu = tk.Frame(body, bg="#111827", width=220)
    menu.pack(side="left", fill="y")

    # ================= CONTENT =================
    content = tk.Frame(body, bg="white")
    content.pack(side="right", fill="both", expand=True)

    # ================= UTIL =================
    def clear_content():
        for widget in content.winfo_children():
            widget.destroy()

    # ================= DASHBOARD =================
    def show_dashboard():
        clear_content()

        # ================= TITLE =================
        tk.Label(
            content,
            text="Dashboard Overview",
            font=("Segoe UI", 20, "bold"),
            bg="white"
        ).pack(pady=20)

        # ================= USER INFO =================
        info_card = tk.Frame(content, bg="#f9fafb", bd=1, relief="solid")
        info_card.pack(fill="x", padx=40, pady=10)

        tk.Label(
            info_card,
            text=f"👤 Logged in as : {username}",
            font=("Segoe UI", 13, "bold"),
            bg="#f9fafb"
        ).pack(anchor="w", padx=20, pady=8)

        tk.Label(
            info_card,
            text=f"🔐 Role : {role.upper()}",
            font=("Segoe UI", 12),
            bg="#f9fafb"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # ================= SYSTEM OVERVIEW =================
        overview_card = tk.Frame(content, bg="white", bd=1, relief="solid")
        overview_card.pack(fill="x", padx=40, pady=20)

        tk.Label(
            overview_card,
            text="🛡 Cyber Threat Monitoring System",
            font=("Segoe UI", 15, "bold"),
            bg="white"
        ).pack(anchor="w", padx=20, pady=10)

        tk.Label(
            overview_card,
            text=(
                "This system monitors employee login activities and detects\n"
                "potential security threats such as:\n\n"
                "• Multiple failed login attempts\n"
                "• Login at unusual hours\n"
                "• Login from new devices\n\n"
                "Risk scores are calculated automatically to identify\n"
                "HIGH and MEDIUM risk employees."
            ),
            font=("Segoe UI", 12),
            bg="white",
            justify="left"
        ).pack(anchor="w", padx=20, pady=10)

        # ================= QUICK RISK SUMMARY =================
        from utils.risk import get_risky_employees

        high_risk, medium_risk = get_risky_employees()

        summary_card = tk.Frame(content, bg="#fef3c7", bd=1, relief="solid")
        summary_card.pack(fill="x", padx=40, pady=20)

        tk.Label(
            summary_card,
            text="⚠ Quick Risk Summary",
            font=("Segoe UI", 15, "bold"),
            bg="#fef3c7"
        ).pack(anchor="w", padx=20, pady=10)

        tk.Label(
            summary_card,
            text=f"🔴 High Risk Employees   : {len(high_risk)}",
            font=("Segoe UI", 12, "bold"),
            fg="red",
            bg="#fef3c7"
        ).pack(anchor="w", padx=30, pady=5)

        tk.Label(
            summary_card,
            text=f"🟠 Medium Risk Employees : {len(medium_risk)}",
            font=("Segoe UI", 12, "bold"),
            fg="orange",
            bg="#fef3c7"
        ).pack(anchor="w", padx=30, pady=5)

        tk.Label(
            summary_card,
            text="👉 Use 'Risk Overview' for detailed analysis",
            font=("Segoe UI", 11),
            bg="#fef3c7"
        ).pack(anchor="w", padx=30, pady=10)
    # ================= SINGLE EMP RISK =================
    def show_single_risk(user):
        clear_content()
        result = calculate_risk(user)

        color = "green"
        if result["status"] == "HIGH RISK":
            color = "red"
        elif result["status"] == "MEDIUM RISK":
            color = "orange"

        tk.Label(
            content,
            text=f"Risk Analysis : {user}",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=20)

        tk.Label(
            content,
            text=f"Risk Score : {result['risk_score']}%",
            font=("Segoe UI", 14, "bold"),
            fg=color,
            bg="white"
        ).pack(pady=5)

        tk.Label(
            content,
            text=f"Status : {result['status']}",
            font=("Segoe UI", 14),
            fg=color,
            bg="white"
        ).pack(pady=5)

        tk.Label(
            content,
            text="Reasons",
            font=("Segoe UI", 13, "bold"),
            bg="white"
        ).pack(pady=10)

        if result["reasons"]:
            for r in result["reasons"]:
                tk.Label(
                    content,
                    text=f"• {r}",
                    font=("Segoe UI", 12),
                    bg="white",
                    anchor="w"
                ).pack(fill="x", padx=40)
        else:
            tk.Label(
                content,
                text="• No suspicious activity detected",
                font=("Segoe UI", 12),
                bg="white"
            ).pack()

    # ================= RISK OVERVIEW =================
    def show_risk_overview():
        clear_content()

        high_risk, medium_risk = get_risky_employees()

        tk.Label(
            content,
            text="Employee Risk Overview",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=20)

        # -------- HIGH RISK --------
        tk.Label(
            content,
            text=f"🔴 HIGH RISK EMPLOYEES ({len(high_risk)})",
            font=("Segoe UI", 14, "bold"),
            fg="red",
            bg="white"
        ).pack(anchor="w", padx=30, pady=10)

        if high_risk:
            for emp in high_risk:
                tk.Button(
                    content,
                    text=f"{emp['username']}  |  {emp['risk_score']}%",
                    font=("Segoe UI", 12),
                    bg="#fee2e2",
                    bd=0,
                    anchor="w",
                    command=lambda u=emp["username"]: show_single_risk(u)
                ).pack(fill="x", padx=40, pady=3)
        else:
            tk.Label(content, text="No high risk users", bg="white").pack(anchor="w", padx=40)

        # -------- MEDIUM RISK --------
        tk.Label(
            content,
            text=f"🟠 MEDIUM RISK EMPLOYEES ({len(medium_risk)})",
            font=("Segoe UI", 14, "bold"),
            fg="orange",
            bg="white"
        ).pack(anchor="w", padx=30, pady=15)

        if medium_risk:
            for emp in medium_risk:
                tk.Button(
                    content,
                    text=f"{emp['username']}  |  {emp['risk_score']}%",
                    font=("Segoe UI", 12),
                    bg="#fff7ed",
                    bd=0,
                    anchor="w",
                    command=lambda u=emp["username"]: show_single_risk(u)
                ).pack(fill="x", padx=40, pady=3)
        else:
            tk.Label(content, text="No medium risk users", bg="white").pack(anchor="w", padx=40)

    # ================= LOGS =================
    def show_logs():
        clear_content()

        import pandas as pd
        from tkinter import ttk

        tk.Label(
            content,
            text="Threat Logs",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        # ================= FILTER BAR =================
        filter_frame = tk.Frame(content, bg="white")
        filter_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_frame, text="Threat Type:", bg="white").pack(side="left", padx=5)

        threat_var = tk.StringVar(value="All")
        threat_cb = ttk.Combobox(
            filter_frame,
            textvariable=threat_var,
            values=["All", "Failed Login", "Unusual Time", "New Device"],
            state="readonly",
            width=15
        )
        threat_cb.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Risk Level:", bg="white").pack(side="left", padx=10)

        risk_var = tk.StringVar(value="All")
        risk_cb = ttk.Combobox(
            filter_frame,
            textvariable=risk_var,
            values=["All", "HIGH", "MEDIUM", "LOW"],
            state="readonly",
            width=12
        )
        risk_cb.pack(side="left", padx=5)

        # ================= TABLE =================
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("Username", "Login Hour", "Failed", "New Device", "Threat", "Risk")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=140)

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ================= LOAD & FILTER =================
        df = pd.read_csv("data/employee_logs.csv")

        def load_data():
            tree.delete(*tree.get_children())

            for _, row in df.iterrows():
                threats = []
                risk = "LOW"

                if row["failed_attempts"] >= 3:
                    threats.append("Failed Login")
                    risk = "MEDIUM"

                if row["login_hour"] < 6 or row["login_hour"] > 22:
                    threats.append("Unusual Time")
                    risk = "MEDIUM"

                if row["new_device"] == "yes":
                    threats.append("New Device")
                    risk = "MEDIUM"

                if row["failed_attempts"] >= 5:
                    risk = "HIGH"

                threat_text = ", ".join(threats) if threats else "Normal"

                # -------- APPLY FILTERS --------
                if threat_var.get() != "All" and threat_var.get() not in threat_text:
                    continue

                if risk_var.get() != "All" and risk_var.get() != risk:
                    continue

                tree.insert(
                    "",
                    "end",
                    values=(
                        row["username"],
                        row["login_hour"],
                        row["failed_attempts"],
                        row["new_device"],
                        threat_text,
                        risk
                    )
                )

        threat_cb.bind("<<ComboboxSelected>>", lambda e: load_data())
        risk_cb.bind("<<ComboboxSelected>>", lambda e: load_data())

        load_data()
    # ================= USERS =================
    def show_users():
        clear_content()

        from utils.auth import get_all_users
        from tkinter import ttk

        tk.Label(
            content,
            text="Registered Users",
            font=("Segoe UI", 18, "bold"),
            bg="white"
        ).pack(pady=15)

        tk.Label(
            content,
            text="Admin can view system users (read-only)",
            font=("Segoe UI", 11),
            fg="gray",
            bg="white"
        ).pack(pady=5)

        # ================= TABLE =================
        table_frame = tk.Frame(content, bg="white")
        table_frame.pack(fill="both", expand=True, padx=30, pady=20)

        columns = ("Username", "Role", "Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)

        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ================= LOAD USERS =================
        users = get_all_users()

        for user in users:
            tree.insert(
                "",
                "end",
                values=(user[0], user[1].upper(), "ACTIVE")
            )

    # ================= MENU BUTTON =================
    def menu_btn(text, cmd):
        return tk.Button(
            menu,
            text=text,
            command=cmd,
            bg="#111827",
            fg="white",
            font=("Segoe UI", 12),
            bd=0,
            activebackground="#1f2933",
            padx=20,
            pady=12,
            anchor="w"
        )

    # ================= MENU =================
    menu_btn("🏠 Dashboard", show_dashboard).pack(fill="x")
    menu_btn("📊 Visual Analytics", open_visual_dashboard).pack(fill="x")
    menu_btn("⚠ Risk Overview", show_risk_overview).pack(fill="x")
    menu_btn("📜 Logs", show_logs).pack(fill="x")

    if role == "admin":
        menu_btn("👤 Users", show_users).pack(fill="x")

    menu_btn("🚪 Logout", logout).pack(side="bottom", fill="x")

    # ================= DEFAULT =================
    show_dashboard()
    dash.mainloop()