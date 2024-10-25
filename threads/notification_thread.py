# threads/notification_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import psutil
import time
import smtplib
from email.mime.text import MIMEText

class NotificationThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, threshold, email):
        super().__init__()
        self.threshold = threshold
        self.email = email
        self._is_running = True

    def run(self):
        while self._is_running:
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.threshold:
                alert_message = f"CPU usage is at {cpu_usage}%"
                self.output.emit(alert_message)
                # Send email alert
                self.send_email(alert_message)
            time.sleep(5)
        self.finished.emit()

    def send_email(self, message):
        try:
            # Configure SMTP server (using Gmail as an example)
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            sender_email = 'your_email@gmail.com'
            sender_password = 'your_email_password'  # Use app password if 2FA is enabled

            msg = MIMEText(message)
            msg['Subject'] = 'Network Alert'
            msg['From'] = sender_email
            msg['To'] = self.email

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [self.email], msg.as_string())
            server.quit()
            self.output.emit("Email alert sent.")
        except Exception as e:
            self.output.emit(f"Failed to send email: {e}")

    def stop(self):
        self._is_running = False
