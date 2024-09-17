from typing import Iterable
import scrapy
from scrapy.http import Response
from ..items import SgiherbItem
from datetime import datetime


class SgIherbSpider(scrapy.Spider):
    name = "sg.iherb"
    allowed_domains = ["sg.iherb.com"]
    start_urls = [
        "https://sg.iherb.com/pr/cococare-100-moroccan-argan-oil-2-fl-oz-60-ml/50488"
    ]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            "https://sg.iherb.com/pr/cococare-100-moroccan-argan-oil-2-fl-oz-60-ml/50488",
            dont_filter=True,
            meta={"impersonate": "chrome110"},
        )

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
