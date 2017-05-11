#!/usr/bin/env python
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
