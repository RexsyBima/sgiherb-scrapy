# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime  #
from sqlalchemy import Boolean, create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


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


class SgiherbSqlAlchemyItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    product_description = Column(String)
    product_overview = Column(String)
    manufacturer = Column(String(50))
    manufacturer_website = Column(String(100))
    rating = Column(Float, nullable=False)
    total_rating = Column(Integer, nullable=False)
    in_stock = Column(Boolean, nullable=False)
    date_scraped = Column(DateTime, default=datetime.now().date())
    img_url = Column(String)
    url = Column(String, unique=True, nullable=False)


engine = create_engine("sqlite:///sgiherb.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
