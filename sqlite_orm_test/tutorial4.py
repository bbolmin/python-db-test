from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import declarative_base, relationship, Session

'''
[ORM 방식 테이블 생성]
- Base 객체를 상속 받는 하위 객체를 정의
'''

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'  # 데이터베이스에서 사용할 테이블 이름입니다.

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


engine = create_engine("sqlite:///:memory:", echo=True)

# ORM으로 선언한 Table(User, Address)을 Database에 생성
Base.metadata.create_all(engine)

user1 = User(name="sandy", fullname="Sandy Cheeks")

with Session(engine) as session:
    session.execute(
        select(User.name, Address).
        where(User.id == Address.user_id).
        order_by(Address.id)
    ).all()
