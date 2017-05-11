import scrapy
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse

class BlogSpider(scrapy.Spider):
    name = 'koniglabs'
    base_url = 'http://koniglabs.ru'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response):
        filename = 'crawl_result//%s.html' % response.url[7:].replace('/', '_')
        with open(filename, 'w') as f:
            f.write(str(response.body))
        self.log('Saved file %s' % filename)

        links = response.css('a::attr(href)').extract()
        for link in links:
            if 'http' in link:
                continue
            print('URL: %s' % link)
            yield scrapy.Request(url=self.base_url+link, callback=self.parse)

