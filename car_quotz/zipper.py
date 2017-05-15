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

import os
import zipfile


class Zipper:
    @staticmethod
    def zip_dir():
        zip_handle = zipfile.ZipFile('car_quotz.zip', 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk('crawl_result/'):
            for file in files:
                zip_handle.write(os.path.join(root, file))
        zip_handle.close()
