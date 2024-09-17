from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from db_to_csv import Base
from dataclasses import dataclass


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


@dataclass
class SgiherbItem:
    title: str
    price: float
    product_description: str
    product_overview: str
    manufacturer: str
    manufacturer_website: str
    rating: float
    total_rating: int
    in_stock: bool
    date_scraped: datetime
    img_url: str
    url: str
