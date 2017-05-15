#!/usr/bin/env python
# This file is part of Car Quotz Scraper by Nikolay Pasko.
#
# Car Quotz Scraper is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Car Quotz Scraper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

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

