from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스에 연결할 엔진 생성
engine = create_engine('sqlite:///example.db', echo=True)

# 세션 생성을 위한 Session 클래스 생성
Session = sessionmaker(bind=engine)

# 모델의 기본 클래스 선언
Base = declarative_base()

# 사용자 모델 정의
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

new_user = User(name='John', age=30)

session = Session()
session.add(new_user)
session.commit()

users = session.query(User).all()
for user in users:
    print(user.name, user.age)

session.close()
