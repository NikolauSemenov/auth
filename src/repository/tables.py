from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean

metadata = MetaData()


Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True),
    Column("password", String),
    Column("is_admin", Boolean, default=False),
    Column("is_active", Boolean, default=False),
)
