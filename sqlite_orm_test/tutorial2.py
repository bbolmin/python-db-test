from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

'''
engine.connect가 아닌 ORM의 Session 객체 사용하기
'''

engine = create_engine("sqlite:///:memory:", echo=True)

# 1. DB 생성
with Session(engine) as session:
    session.execute(text("CREATE TABLE some_table (x int, y int)"))
    session.commit()

# 2. 데이터 삽입
with Session(engine) as session:
    session.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    session.commit()

# 3. 데이터 조회
with Session(engine) as session:
    result = session.execute(text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y").bindparams(y=0))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
