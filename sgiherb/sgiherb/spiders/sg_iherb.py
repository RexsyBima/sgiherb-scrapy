from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from scrapy.http import Response
from ..items import SgiherbItem
from datetime import datetime
import random


class SgIherbSpider(CrawlSpider):
    browser_names = ["chrome124", "chrome123", "chrome120", "chrome110"]
    name = "sg.iherb"
    allowed_domains = ["sg.iherb.com"]
    start_urls = ["https://sg.iherb.com/new-products"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    rules = [
        Rule(link_extractor=LinkExtractor(allow=r"p="), follow=True),
        Rule(
            link_extractor=LinkExtractor(allow=r"/pr/"),
            callback="parse",
            follow=True,
            process_request="enable_impersonate",
        ),
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                dont_filter=True,
                meta={"impersonate": self.get_impersonate_cffi()},
            )

    def enable_impersonate(self, request, response):
        request.meta["impersonate"] = "chrome110"
        return request

    def parse(self, response: Response):
        title = response.css("h1#name ::text").get()
        price = response.css("div#price div.price-inner-text p ::text").get()
        product_description = response.css("ul#product-specs-list li ::text").getall()
        product_overview = response.css("div.inner-content ::text").getall()
        manufacturer = response.css("div#brand span ::text").getall()
        manufacturer_website = response.css(
            "section.col-xs-24.product-overview-link a ::attr(href)"
        ).get()
        rating = response.css(
            "div.product-review-summary-v2 a.average-rating.scroll-to ::text"
        ).get()
        total_rating = response.css("div.product-review-summary-v2 span ::text").get()
        in_stock = response.css("strong.text-primary ::text").get()
        date_scraped = datetime.now().date()
        url = response.url
        img_url = response.css("img#iherb-product-image ::attr(src)").get()
        item = SgiherbItem(
            title=title,
            price=price,
            product_description=product_description,
            product_overview=product_overview,
            manufacturer=manufacturer,
            manufacturer_website=manufacturer_website,
            rating=rating,
            total_rating=total_rating,
            in_stock=in_stock,
            date_scraped=date_scraped,
            url=url,
            img_url=img_url,
        )

        yield item

    def get_impersonate_cffi(self):
        return random.choice(self.browser_names)
