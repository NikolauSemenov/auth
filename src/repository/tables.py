from sqlalchemy import Table, MetaData, Column, Integer, String

metadata = MetaData()


Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("password", String),
)
