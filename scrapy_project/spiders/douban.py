import scrapy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.css('.grid_view li')
        for li in movie_list:
            yield {
                'serial_number': li.css('em::text').get(),
                'movie_name': li.css('.title::text').get(),
                'introduce': li.css('.bd > p:first-child::text').get().strip(),
                'rating': li.css('.rating_num::text').get(),
                'evaluate':
                li.css('.star span:last-child::text').re_first(r'^\d+'),
                'description': li.css('.inq::text').get()
            }

        try:
            yield response.follow(response.css('.next a')[0])
        except IndexError:
            pass
