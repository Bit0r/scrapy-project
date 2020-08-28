import scrapy

from env import game


class GameSpider(scrapy.Spider):
    name = 'game'
    allowed_domains = [game['domain']]
    url = game['url']
    cookies = game['cookies']

    def start_requests(self):
        for aid in game['aids']:
            yield scrapy.Request(self.url + str(aid), cookies=self.cookies)

    def parse(self, response):
        downlink = response.css('tr:first-child a::attr(href)').get()

        if downlink is not None:
            activation = response.css(
                'tr:last-child > td:last-child').re_first('\d{6}')

            bonus = response.css('tr:nth-child(2) a::attr(href)').get().strip()
            if bonus == '敬请期待':
                bonus = None

            yield {
                'id': response.url.split('?aid=')[1],
                'download': downlink.strip(),
                'bonus': bonus,
                'activation': activation
            }
