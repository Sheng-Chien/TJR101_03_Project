from sqlalchemy import create_engine, Table, MetaData, update
from sqlalchemy import and_
from sqlalchemy.dialects.mysql import insert
from airflow.hooks.base import BaseHook

db_conn = BaseHook.get_connection("TJR101_DB")
engine = create_engine(db_conn.get_uri())

# 建立資料表映射
metadata = MetaData()
metadata.reflect(bind=engine)
merge_table = metadata.tables['campground_merge']
MYSQL_CONN = engine.connect()

def update_with_filter(table, filter, values):
    stmt = (
        update(table)
        .where(and_(*[
            table.c[col] == val for col, val in filter.items()
        ]))
        .values(**values)
    )
    return stmt

def insert_with_values(table, values):
    stmt = insert(table).values(**values)
    return stmt

def upsert_with_values(table, values):
    stmt = insert(table).values(values)
    stmt = stmt.on_duplicate_key_update(name=stmt.inserted.name)
    return stmt