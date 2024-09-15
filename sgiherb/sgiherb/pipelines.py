# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SgiherbPipeline:
    def process_item(self, item, spider):
        item["title"] = item["title"].strip()
        item["price"] = float(item["price"].strip().replace("SG$", ""))
        item["product_description"] = self.parsing_whitespaces(
            item["product_description"]
        )
        item["product_overview"] = self.parsing_product_overview(
            self.parsing_whitespaces(item["product_overview"])
        )
        item["manufacturer"] = self.parsing_whitespaces(item["manufacturer"])[0]
        item["rating"] = float(item["rating"])
        item["total_rating"] = int(item["total_rating"].replace(",", ""))
        item["in_stock"] = self.check_stock(item["in_stock"])
        return item

    def parsing_whitespaces(self, value: list[str]):
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


# todo -> create new pipeline, connect kan ke sqlalchemy untuk dimasukan kedalam db
# todo -> lakuin paginasi halaman
# todo -> bikin script baru -> ngambil data dari database diconvertt ke excel atau csv
