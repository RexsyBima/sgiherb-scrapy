# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime  #


class SgiherbItem(scrapy.Item):
    title: str = scrapy.Field()
    price: float = scrapy.Field()
    product_description: str | list = (
        scrapy.Field()
    )  # out = [s for s in strings if len(s.strip()) > 0]
    product_overview: str = scrapy.Field()
    manufacturer: str = scrapy.Field()
    manufacturer_website: str = scrapy.Field()
    rating: float = scrapy.Field()
    total_rating: int = scrapy.Field()  # int(x.replace(",", ""))
    in_stock: bool = scrapy.Field()
    date_scraped: datetime = scrapy.Field()
    img_url = scrapy.Field()
    url = scrapy.Field()

    # define the fields for your item here like:
    # name = scrapy.Field()
