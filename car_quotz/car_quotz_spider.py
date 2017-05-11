import os
import scrapy
import pdfkit
import time
import datetime

from bs4 import BeautifulSoup
from subprocess import call

class CarQuotzSpider(scrapy.Spider):
    name = 'car_quotz'
    base_url = 'http://www.quotz.com.sg'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url + '/auction/listing.php', callback=self.parse)

    def parse(self, response):
        # links = response.xpath('//a[contains(@href, "info.php")]/@href').extract()
        closed_links = response.xpath(
            '//div[./div/img/@title="closed"]/div/a[@href[starts-with(., "info.php")] and img[contains(@title, "closed")]]/@href').extract()
        sold_images = response.xpath('//img[contains(@title, "sold")]').extract()
        pagebar = response.xpath('//a[@class="pagebar"]/@href').extract()
        next_page = pagebar[len(pagebar) - 1]
        if len(closed_links) > 0:
            for link in set(closed_links):
                self.log('* INFO: Closed car found: %s' % link)
                yield scrapy.Request(url=self.base_url + '/auction/' + link, callback=self.parse_inner)
            self.log('* INFO: Next page: %s' % next_page)
        if len(sold_images) > 0:
            return
        yield scrapy.Request(url=self.base_url + next_page, callback=self.parse)

    def parse_inner(self, response):
        main_table = response.xpath('//div[@class="infobox"]').extract()[0]
        car_name1 = response.xpath('//div[@class="info_header"]/em/a/text()').extract()[0]
        car_name2 = response.xpath('//div[@class="info_header"]/em/text()').extract()[0]
        car_name = (car_name1 + car_name2).replace('/', '.')
        # print("*INFO: %s" % car_name)
        now = datetime.datetime.utcnow()
        html_text = self.morph_html(main_table)
        html_file_name = 'crawl_result//%s_%s.html' % (car_name, now.date())
        self.save_html(html_file_name, html_text)
        pdf_file_name = 'crawl_result//%s_%s.pdf' % (car_name, now.date())
        self.save_pdf(html_file_name, pdf_file_name)
        os.remove(html_file_name)
        time.sleep(5)

    def save_html(self, html_file_name, html_text):
        with open(html_file_name, "wt") as f:
            f.write(html_text)

    def save_pdf_cuty(self, html_file_name, pdf_file_name):
        call(['xvfb-run', '--server-args="-screen 0, 1280x1200x24"', 'cutycapt --url=file:////'+html_file_name+' --out='+pdf_file_name])

    def save_pdf(self, html_file_name, pdf_file_name):
        try:
            pdfkit.from_file(html_file_name, pdf_file_name)
            self.log('* Saved file %s' % pdf_file_name)
        except:
            self.log('** ERROR converting to pdf')
            self.log('* Saved file %s' % html_file_name)

    @staticmethod
    def morph_html(main_table):
        html_text = '<html><body>%s</body></html>' % main_table
        html_soup = BeautifulSoup(html_text, "lxml")

        layers = html_soup.body.find_all('div', attrs={'id': 'Layers'})
        for layer in layers:
            layer.decompose()
        frames = html_soup.body.find_all('div', attrs={'id': 'frames'})
        for frame in frames:
            frame.decompose()
        scripts = html_soup.body.find_all('script')
        for script in scripts:
            script.decompose()
        thumb_table = html_soup.body.find('table', attrs={'id': 'thumbn_table'})
        thumb_table.decompose()

        return html_soup.prettify()
