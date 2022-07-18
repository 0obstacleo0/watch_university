import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

# 環境変数からパラメータ取得
# FROM_ADDRESS = os.environ["FROM_ADDRESS"]
# TO_ADDRESS = os.environ["TO_ADDRESS"]
# PASSWORD = os.environ["PASSWORD"]

# メール送信
def send_mail(subject, text):
    smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpobj.starttls()
    smtpobj.login(FROM_ADDRESS, PASSWORD)

    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"] = FROM_ADDRESS
    msg["To"] = TO_ADDRESS
    msg["Date"] = formatdate()

    smtpobj.send_message(msg)
    smtpobj.close()
