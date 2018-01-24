import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class mailer():
    def __init__(self, subject):
        self.me = 'sanketm221995@gmail.com'
        self.you = 'sanket_m@protonmail.com'
        self.msg = MIMEMultipart('alternative')
        self.subject = subject

    @staticmethod
    def send_mail_ttls(sender, to_send, email):
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('sanketm221995@gmail.com', 'Macwiz123')
        mail.sendmail(from_addr=sender, to_addrs=to_send, msg=email.as_string())
        mail.quit()

    def send_html_email(self):
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.me
        self.msg['to'] = self.you
        html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Intern</title>
    <style>
        * {margin: 0; padding: 0;}

div {
  margin: 20px;
}

ul {
  list-style-type: none;
  width: 500px;
}

h3 {
  font: bold 20px/1.5 Helvetica, Verdana, sans-serif;
}

li img {
  float: left;
  margin: 0 15px 0 0;
}

li p {
  font: 200 12px/1.5 Georgia, Times New Roman, serif;
}

li {
  padding: 10px;
  overflow: auto;
}

li:hover {
  background: #eee;
  cursor: pointer;
}
    </style>
</head>
<body>
<div>
  <ul>
    <li>
      <img src="http://lorempixum.com/100/100/nature/1" />
      <h3>Headline</h3>
      <p>Lorem ipsum dolor sit amet...</p>
    </li>

    <li>
      <img src="http://lorempixum.com/100/100/nature/2" />
      <h3>Headline</h3>
      <p>Lorem ipsum dolor sit amet...</p>
    </li>

    <li>
      <img src="http://lorempixum.com/100/100/nature/3" />
      <h3>Headline</h3>
      <p>Lorem ipsum dolor sit amet...</p>
    </li>

    <li>
      <img src="http://lorempixum.com/100/100/nature/4" />
      <h3>Headline</h3>
      <p>Lorem ipsum dolor sit amet...</p>
    </li>
  </ul>
</div>
</body>
</html>
        """
        part1 = MIMEText('Hii', 'plain')
        part2 = MIMEText(html, 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)
        self.send_mail_ttls(sender=self.me, to_send=self.you, email=self.msg)
