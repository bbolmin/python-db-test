from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, delete, select
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

'''
[ORM 방식 테이블 생성]
- Base 객체를 상속 받는 하위 객체를 정의

[ORM 방식 쿼리]
- execute가 아닌 
'''

# 엔진 생성
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # 사용자와 게시물 간의 관계 정의
    posts = relationship("Post", back_populates="author")


# 게시물 모델 정의
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))

    # 게시물과 사용자 간의 관계 정의
    author = relationship("User", back_populates="posts")


# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

session = Session()
user1 = User(name='John')
user2 = User(name='Alice')
session.add(user1)
session.add(user2)

post1 = Post(title='First Post', content='Content of the first post', author=user1)
post2 = Post(title='Second Post', content='Content of the second post', author=user2)
session.add(post1)
session.add(post2)

# 변경 내용 커밋
session.commit()

# 모든 사용자와 게시물 검색
'''
all() 사용시
- ChunkedIteratorResult -> [(<__main__.User object at 0x000001954EDCB950>,)] 와 같이 list 형식으로 반환
'''
users = session.query(User).where(User.name != 'test').all()
for user in users:
    for post in user.posts:
        print(f"[test1][{user.name}] {post.title} - {post.content}")

users = session.execute(select(User).where(User.name != 'test')).all()
for user in users:
    print(f'[test2] {user[0].name}')

users = session.execute(select(User).where(User.posts.any(Post.title != 'test'))).all()
for user in users:
    print(f'[test2] {user[0].name}')

# 삭제하기 (객체 사용)
user = session.get(User, 1)
print(user in session)  # True
session.delete(user)
session.commit()
print(user in session)  # False (expired 상태)

# 삭제하기 (ORM 사용)
session.execute(delete(User).where(User.name == "John"))

# 롤백하기
session.rollback()

# 세션 닫기
session.close()
