import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import Config

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = Config.EMAIL_USER
        self.password = Config.EMAIL_PASS
        self.enabled = bool(self.email and self.password and self.password != 'your_16_char_app_password')

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send an email using SMTP"""
        # Skip if email is not configured
        if not self.enabled:
            print(f"[Email Service] Skipped - not configured. Would send to: {to_email}")
            return True  # Return True to not break the flow
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject

            # Add body to email
            msg.attach(MIMEText(body, 'plain'))

            # Create SMTP session
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.email, self.password)

            # Convert message to string and send
            text = msg.as_string()
            server.sendmail(self.email, to_email, text)
            server.quit()

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send a welcome email to new users"""
        subject = "Welcome to Worlds AI Bot!"
        body = f"""
        Hi {user_name},

        Welcome to Worlds AI Bot! We're excited to have you on board.

        Thank you for joining our learning platform.

        Best regards,
        Worlds AI Bot Team
        """
        return self.send_email(to_email, subject, body)

    def send_password_reset_email(self, to_email: str, reset_link: str) -> bool:
        """Send a password reset email"""
        subject = "Password Reset Request"
        body = f"""
        Hi,

        You have requested to reset your password. Please click the link below to reset your password:

        {reset_link}

        If you did not request this, please ignore this email.

        Best regards,
        Worlds AI Bot Team
        """
        return self.send_email(to_email, subject, body)