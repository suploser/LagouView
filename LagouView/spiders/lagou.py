# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LagouView.items import LagouItemLoader,LagouViewItem

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 3,
        'DOWNLOADER_MIDDLEWARES': {
            'LagouView.middlewares.LagouRandomUserAgentMiddleware': 1,
        },
            'ITEM_PIPELINES': {
                'LagouView.pipelines.LagouviewPipeline':1,
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
        }
    }

    rules = (
        Rule(LinkExtractor(allow='jobs/\d+.html'), follow=True, callback='parse_job'),
        Rule(LinkExtractor(allow='zhaopin/.*'), ),
        Rule(LinkExtractor(allow='gongsi/\d+.html'))
    )

    def parse_job(self, response):
       Item_loader = LagouItemLoader(item=LagouViewItem(), response=response)
       Item_loader.add_css('job_name', '.position-head .name::text')
       Item_loader.add_xpath('work_years', '//*[@class="job_request"]/p/span[3]/text()')
       Item_loader.add_xpath('degree', '//*[@class="job_request"]/p/span[4]/text()')
       Item_loader.add_xpath('job_type', '//*[@class="job_request"]/p/span[5]/text()')
       Item_loader.add_xpath('job_address', '//*[@class="job_request"]/p/span[2]/text()')
       Item_loader.add_xpath('salary', '//*[@class="job_request"]/p/span[1]/text()')
       Item_loader.add_css('welfare', '.job-advantage p::text')
       Item_loader.add_css('company', '#job_company a img::attr(alt)')
       item = Item_loader.load_item()

       return item