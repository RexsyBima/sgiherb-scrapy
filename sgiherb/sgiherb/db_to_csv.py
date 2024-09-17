import pandas as pd
from db_to_csv.utils import get_current_date

from db_to_csv import session
from db_to_csv.models import SgiherbSqlAlchemyItem, SgiherbItem


if __name__ == "__main__":
    # df = pd.read_sql_table("items", session.bind)
    all_data = session.query(SgiherbSqlAlchemyItem).all()
    all_data = [item.__dict__ for item in all_data]
    for i in all_data:
        del i["_sa_instance_state"]
        del i["id"]
    items = [SgiherbItem(**i) for i in all_data]
    df = pd.DataFrame(items)
    df.to_csv(f"sgiherb-{get_current_date()}.csv", index=False)
