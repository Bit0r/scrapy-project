import scrapy
from scrapy.utils.response import open_in_browser

import env


class XgglSpider(scrapy.Spider):
    name = 'xggl'
    allowed_domains = ['xggl.hnie.edu.cn']

    def start_requests(self):
        yield scrapy.FormRequest('http://xggl.hnie.edu.cn/website/login',
                                 callback=self.parse_login,
                                 formdata={
                                     'username': env.xggl_user,
                                     'password': env.xggl_password_md5
                                 })

    def parse_login(self, response):
        with open('login.txt', 'wb') as f:
            f.write(response.body)
        yield scrapy.FormRequest(
            'http://xggl.hnie.edu.cn/content/student/temp/zzdk',
            formdata=env.xggl_formdata)

    def parse(self, response):
        open_in_browser(response)
