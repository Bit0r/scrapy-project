import scrapy
from scrapy.utils.response import open_in_browser

from env import xggl


class XgglSpider(scrapy.Spider):
    name = 'xggl'
    allowed_domains = ['xggl.hnie.edu.cn']

    def start_requests(self):
        yield scrapy.FormRequest('http://xggl.hnie.edu.cn/website/login',
                                 self.parse_login,
                                 formdata={
                                     'username': xggl['user'],
                                     'password': xggl['password_md5']
                                 })

    def parse_login(self, response):
        with open('login.txt', 'wb') as f:
            f.write(response.body)
        yield scrapy.FormRequest(
            'http://xggl.hnie.edu.cn/content/student/temp/zzdk',
            formdata=xggl['formdata'])

    def parse(self, response):
        open_in_browser(response)
