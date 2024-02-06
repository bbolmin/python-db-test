from sqlalchemy import text
from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:", echo=True)

#1. DB 생성
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.commit()

#2. 데이터 삽입
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}]
    )
    conn.commit()

#3. 데이터 삽입 (자동으로 commit)
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}]
    )


#4. 데이터 조회
with engine.connect() as conn:
    # result = conn.execute(text("SELECT x, y FROM some_table"))
    result = conn.execute(text("SELECT x, y FROM some_table"))

    for x, y in result:
        print(f"x: {x}  y: {y}")

#4. 데이터 조회 (sql문 인자 넘기기)
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT x, y FROM some_table WHERE y > :y"),  # 콜론 형식(:)으로 받습니다.
        {"y": 2}  # 사전 형식으로 넘깁니다.
    )
    for row in result:
       print(f"x: {row.x}  y: {row.y}")