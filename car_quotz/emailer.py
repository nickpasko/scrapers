import smtplib
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename


class Emailer:
    @staticmethod
    def send():
        filename = 'car_quotz.zip'
        from_addr = 'nikolay.pasko@koniglabs.ru'
#        to_addr = 'hiteshsc@gmail.com'
        to_addr = 'nickpasko@mail.ru'
        server = 'localhost'

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = str(datetime.now())
        msg['Subject'] = 'Recently closed deals'

        msg.attach(MIMEText(str(datetime.now())))

        with open(filename, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(filename)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
            msg.attach(part)

        s = smtplib.SMTP(server)
        s.sendmail(from_addr, [to_addr], msg.as_string())
        s.quit()

