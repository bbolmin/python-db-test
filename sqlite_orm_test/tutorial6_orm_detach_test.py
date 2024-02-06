from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, delete
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# 엔진 생성
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

session = Session()
user1 = User(name='John')
session.add(user1)
session.add(user1) # 동일 객체를 여러번 add 해도 하나만 반영됨


session.commit()
print(user1 in session) #True
print(user1.__dict__) #{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x00000225AB431010>, 'name': 'John'}
session.close() #close()로 인해 user1은 detach됨

session = Session()
# user1은 detach된 상태 (user1.name 와 같은 조회 불가)
print(user1 in session) # False
print(user1.__dict__) # {'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x00000225AB431010>}

# session.add로 다시 attach
session.add(user1)
print(user1 in session) # True
print(user1.__dict__)
session.close()

users = session.query(User).all()
for user in users:
    print(f"[+] User: {user.name}")