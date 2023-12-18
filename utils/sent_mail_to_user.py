from smtplib import SMTP
import math
import random
import os
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

mail_from = "dharmikanghan09@gmail.com"


def generate_otp():
    digits = "0123456789"

    otp = ""

    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]

    return otp


def sent_otp(mail_to):
    __otp = generate_otp()

    content = f"{__otp} is your OTP. \nPlease do not share it with anyone."

    msg = EmailMessage()

    msg.set_content(content)

    msg["Subject"] = "OTP Verification"
    msg["From"] = mail_from
    msg["To"] = mail_to

    sent = SMTP("smtp.gmail.com", 587)
    sent.starttls()
    sent.login(mail_from, password=os.environ.get("EMAIL_PASSWORD"))
    sent.send_message(msg)
    return __otp
