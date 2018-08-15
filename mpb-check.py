import scrapy
import os


class MBPSpider(scrapy.Spider):
    name = "quantities"

    def start_requests(self):
        url = os.environ.get('MPB_URL')
        urls = [url, ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        quantity = int(response.css('strong.www-results-count::text').extract_first())

        if quantity > 0:
            # Send an email
            pass

        self.log('Quantity available: %s' % quantity)
