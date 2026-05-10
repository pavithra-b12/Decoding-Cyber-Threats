import pandas as pd
from utils.email_alert import send_risk_report

DATA_PATH = "data/employee_logs.csv"
REPORT_PATH = "data/employee_risk_report.xlsx"

def get_risky_employees():
    import pandas as pd

    DATA_PATH = "data/employee_logs.csv"
    df = pd.read_csv(DATA_PATH)

    def calculate_score(row):
        score = 0
        if row["failed_attempts"] >= 5:
            score += 40
        if row["login_hour"] < 6 or row["login_hour"] > 22:
            score += 30
        if row["new_device"] == "yes":
            score += 30
        return score

    df["risk_score"] = df.apply(calculate_score, axis=1)

    high_risk = []
    medium_risk = []

    for user in df["username"].unique():
        user_rows = df[df["username"] == user]

        max_score = user_rows["risk_score"].max()

        if max_score >= 70:
            high_risk.append({
                "username": user,
                "risk_score": max_score,
                "status": "HIGH RISK"
            })

        elif max_score >= 40:
            medium_risk.append({
                "username": user,
                "risk_score": max_score,
                "status": "MEDIUM RISK"
            })

    return high_risk, medium_risk


def calculate_risk(username):
    df = pd.read_csv(DATA_PATH)
    emp = df[df["username"] == username]

    if emp.empty:
        return {"username": username, "risk_score": 0, "status": "NO DATA", "reasons": []}

    failed = emp["failed_attempts"].sum()
    odd_time = emp[(emp["login_hour"] < 6) | (emp["login_hour"] > 22)].shape[0]
    new_device = emp[emp["new_device"] == "yes"].shape[0]

    risk_score = (failed * 10) + (odd_time * 15) + (new_device * 20)

    reasons = []
    if failed >= 5:
        reasons.append("Multiple failed login attempts")
    if odd_time > 0:
        reasons.append("Login at unusual hours")
    if new_device > 0:
        reasons.append("Login from new device")

    if risk_score >= 70:
        status = "HIGH RISK"
    elif risk_score >= 40:
        status = "MEDIUM RISK"
    else:
        status = "LOW RISK"

    return {
        "username": username,
        "risk_score": risk_score,
        "status": status,
        "reasons": reasons
    }


def generate_risk_report():
    df = pd.read_csv(DATA_PATH)

    def score(row):
        s = 0
        if row["failed_attempts"] >= 5:
            s += 40
        if row["login_hour"] < 6 or row["login_hour"] > 22:
            s += 30
        if row["new_device"] == "yes":
            s += 30
        return s

    df["risk_score"] = df.apply(score, axis=1)
    df["risk_status"] = df["risk_score"].apply(
        lambda x: "HIGH" if x >= 70 else "MEDIUM" if x >= 40 else "LOW"
    )

    high = df[df["risk_status"] == "HIGH"]
    medium = df[df["risk_status"] == "MEDIUM"]

    with pd.ExcelWriter(REPORT_PATH, engine="openpyxl") as writer:
        high.to_excel(writer, sheet_name="HIGH_RISK", index=False)
        medium.to_excel(writer, sheet_name="MEDIUM_RISK", index=False)

    return REPORT_PATH, len(high), len(medium)


def process_and_send_risk_report():
    print("▶ Risk report process started")

    report_path, high_cnt, medium_cnt = generate_risk_report()

    print("High Risk Count   :", high_cnt)
    print("Medium Risk Count :", medium_cnt)

    send_risk_report(
        subject="🚨 Employee Cyber Risk Report",
        body=f"""
Cyber Threat Monitoring Alert

High Risk Employees   : {high_cnt}
Medium Risk Employees : {medium_cnt}

Please find attached detailed Excel report.
""",
        attachment_path=report_path
    )

    return "✅ Risk report email sent successfully"