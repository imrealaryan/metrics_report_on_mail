#!/usr/bin/env python3
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory()
    ram_total = round(memory.total / (1024**3), 2)
    ram_used = round(memory.used / (1024**3), 2)
    ram_percent = memory.percent

    disk = psutil.disk_usage('/')
    disk_total = round(disk.total / (1024**3), 2)
    disk_used = round(disk.used / (1024**3), 2)
    disk_percent = disk.percent

    return {
        "CPU Usage (%)": cpu_usage,
        "RAM (Used/Total GB)": f"{ram_used}/{ram_total} ({ram_percent}%)",
        "Disk (Used/Total GB)": f"{disk_used}/{disk_total} ({disk_percent}%)"
    }

def send_email(usage, sender_email, sender_password, receiver_email, smtp_server="smtp.gmail.com", smtp_port=587):
    subject = "System Usage Report"

    # Build message
    body = "\n".join([f"{k}: {v}" for k, v in usage.items()])
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    usage = get_system_usage()
    for k, v in usage.items():
        print(f"{k}: {v}")

    # ===== EDIT THESE =====
    sender_email = "xyz"
    sender_password = "xyz"  # use app password, not real password
    receiver_email = "xyz"

    send_email(usage, sender_email, sender_password, receiver_email)
