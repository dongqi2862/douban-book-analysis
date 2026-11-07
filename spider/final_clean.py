import pymysql
import re

conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="txy20060411",
    database="douban_book",
    charset="utf8mb4"
)
cur = conn.cursor()

create_final = """
CREATE TABLE IF NOT EXISTS final_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(300),
    author_country VARCHAR(50),
    score FLOAT,
    publisher TEXT,
    comment_count INT,
    pub_year INT,
    price_num FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cur.execute(create_final)
cur.execute("TRUNCATE TABLE final_book;")
conn.commit()

cur.execute("SELECT book_name, author, score, publisher, comment_count, pub_year, price_num FROM clean_book;")
rows = cur.fetchall()

insert_sql = """
INSERT INTO final_book
(book_name, author, author_country, score, publisher, comment_count, pub_year, price_num)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

dynasties = {"汉", "唐", "宋", "元", "明", "清"}
success = 0

for row in rows:
    book_name, raw_author, score, publisher, comment_count, pub_year, price_num = row

    raw_author_trim = raw_author.strip()
    # 加入中文全角括号：（ ），同时兼容 []【】()
    bracket_match = re.match(r"^[\[(【（](.*?)[\])】）]", raw_author_trim)

    if bracket_match:
        tag = bracket_match.group(1).strip()
        real_author = re.sub(r"^[\[(【（].*?[\])】）]", "", raw_author_trim).strip()
        if tag in dynasties:
            country = "中"
        else:
            country = tag
    else:
        country = "中"
        real_author = raw_author_trim

    if price_num is not None:
        price_num = float(price_num)

    one = (book_name, real_author, country, score, publisher, comment_count, pub_year, price_num)
    cur.execute(insert_sql, one)
    success += 1

conn.commit()
print(f"✅清洗完成，写入 {success} 条到 final_book")

cur.close()
conn.close()
