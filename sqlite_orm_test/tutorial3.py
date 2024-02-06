from sqlalchemy import MetaData, create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey

metadata = MetaData()
user_table = Table(
    'user_account',  # table 이름
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String),
)

engine = create_engine("sqlite:///:memory:", echo=True)

# 선언한 Table DB에 생성
metadata.create_all(engine)

