import pandas as pd
from db_to_csv.models import SgiherbSqlAlchemyItem, SgiherbItem
from db_to_csv import session
from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    # df = pd.read_sql_table("items", session.bind)
    all_data = session.query(SgiherbSqlAlchemyItem).all()
    all_data = [item.__dict__ for item in all_data]
    for i in all_data:
        del i["_sa_instance_state"]
        del i["id"]
    items = [SgiherbItemDataclass(**i) for i in all_data]
    df = pd.DataFrame(items)
    df.to_csv(f"sgiherb-{get_current_date()}.csv", index=False)
