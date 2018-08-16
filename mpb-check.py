import scrapy
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


def send_email(quantity):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    to_email = Email(os.environ.get('EMAIL_TO_NOTIFY'))
    subject = "MPB Check: the item you are monitoring is available"
    message = 'There are {0} items available at {1}'.format(quantity, os.environ.get('MPB_URL'))
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


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
            send_email(quantity)

        self.log('Quantity available: %s' % quantity)
