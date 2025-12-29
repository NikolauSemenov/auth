from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean

metadata = MetaData()


Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, unique=True, index=True, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String, nullable=False),
    Column("is_admin", Boolean, default=False),
    Column("is_active", Boolean, default=False),
)
