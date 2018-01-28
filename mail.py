import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template


class mailer():
    def __init__(self, subject):
        self.me = 'sanket.mokashi95@gmail.com'
        self.you = 'sanket.mokashi95@gmail.com'
        self.msg = MIMEMultipart('alternative')
        self.subject = subject

    @staticmethod
    def send_mail_ttls(sender, to_send, email):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('sanket.mokashi95@gmail.com', 'macwiz123')
        mail.sendmail(from_addr=sender, to_addrs=to_send, msg=email.as_string())
        mail.quit()

    def send_html_email(self, topics, details):
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.me
        self.msg['to'] = self.you
        html = render_template(os.path.join(os.getcwd(), 'test report.html'), topics=topics, details=details)
        part1 = MIMEText('Hii', 'plain')
        part2 = MIMEText(html, 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)
        self.send_mail_ttls(sender=self.me, to_send=self.you, email=self.msg)
