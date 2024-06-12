import smtplib
import getpass
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
    def __init__(self) -> None:
        self.verify_code = None

    def generate_password(self):
        self.verify_code = str(random.randint(100000, 999999))
        return self.verify_code

    def send_mail(self, email, vCode):
        subject = 'Email Verification Code'
        body = f'Your email verification code is {vCode}'

        body_html = f"""
        <html>
        <body>
            <p><strong>Email Verification Code</strong></p>
            <p>Your email verification code is: <span style="font-weight: bold; font-size: 16px;">{vCode}</span></p>
            <p><img src="image/company_logo.png" alt="Company Logo"></p>
        </body>
        </html>
        """

        sender_mail = 'udehdinobi@gmail.com'
        sender_pass = 'xcpp mdno byuu ovlu'

        message = MIMEMultipart("alternative")
        # message2 = f'Subject: {subject}\n\n{body}'
        message["Subject"] = subject
        message["From"] = sender_mail
        message["To"] = email
        message.attach(MIMEText(body, "plain"))
        message.attach(MIMEText(body_html, "html"))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.ehlo()
        session.starttls()
        session.login(sender_mail, sender_pass)
        session.sendmail(
            from_addr=sender_mail,
            to_addrs=email,
            msg=message.as_string()
        )
        session.quit()
