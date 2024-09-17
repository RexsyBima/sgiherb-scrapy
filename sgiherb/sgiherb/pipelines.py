# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import session, SgiherbSqlAlchemyItem


class SgiherbPipeline:
    def process_item(self, item, spider):
        item["title"] = item["title"].strip()
        item["price"] = float(item["price"].strip().replace("SG$", ""))
        item["product_description"] = self.parsing_whitespaces_to_string(
            item["product_description"]
        )
        item["product_overview"] = self.parsing_product_overview(
            self.parsing_whitespaces_to_list(item["product_overview"])
        )
        item["manufacturer"] = self.parsing_whitespaces_to_string(item["manufacturer"])[
            0
        ]
        item["rating"] = float(item["rating"])
        item["total_rating"] = int(item["total_rating"].replace(",", ""))
        item["in_stock"] = self.check_stock(item["in_stock"])
        return item

    def parsing_whitespaces_to_string(self, value: list[str]):
        output = [v.strip() for v in value if len(v.strip()) > 0]
        return ".".join(output)

    def parsing_whitespaces_to_list(self, value):
        output = [v.strip() for v in value if len(v.strip()) > 0]
        return output

    def check_stock(self, value):
        value = value.strip()
        match value:
            case "In stock":
                return True
            case _:
                return False

    def parsing_product_overview(self, value):
        return "\n".join(value)


class DbPipeline:
    def open_spider(self, spider):
        self.session = session

    def process_item(self, item, spider):
        product = SgiherbSqlAlchemyItem(**item)
        product_exist = (
            self.session.query(SgiherbSqlAlchemyItem).filter_by(url=product.url).first()
        )
        if product_exist:
            self.update_item(product_exist, product)
        self.session.add(product)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()

    def update_item(
        self, product_exist: SgiherbSqlAlchemyItem, item: SgiherbSqlAlchemyItem
    ):
        product_exist.title = item.title
        product_exist.price = item.price
        product_exist.product_description = item.product_description
        product_exist.product_overview = item.product_overview
        product_exist.manufacturer = item.manufacturer
        product_exist.manufacturer_website = item.manufacturer_website
        product_exist.rating = item.rating
        product_exist.total_rating = item.total_rating
        product_exist.in_stock = item.in_stock
        product_exist.date_scraped = item.date_scraped
        product_exist.img_url = item.img_url
        product_exist.url = item.url
        self.session.commit()


# todo -> create new pipeline, connect kan ke sqlalchemy untuk dimasukan kedalam db v
# todo -> lakuin paginasi halaman
# todo -> bikin script baru -> ngambil data dari database diconvertt ke excel atau csv
