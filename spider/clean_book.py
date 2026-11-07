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

# 重新创建干净的clean_book表，这里每个字段名手敲，杜绝复制来的隐形符号
create_table_sql = """
CREATE TABLE IF NOT EXISTS clean_book (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_name VARCHAR(255) NOT NULL,
    author VARCHAR(300),
    score FLOAT,
    publisher TEXT,
    publish_time VARCHAR(100),
    comment_count INT,
    price VARCHAR(50),
    pub_year INT,
    price_num FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
cur.execute(create_table_sql)
cur.execute("TRUNCATE TABLE clean_book;")
conn.commit()

cur.execute("SELECT * FROM book_info;")
all_rows = cur.fetchall()
print(f"原始总条数：{len(all_rows)}")

insert_sql = """
INSERT INTO clean_book
(book_name, author, score, publisher, publish_time, comment_count, price, pub_year, price_num)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

success = 0
bad_items = []

for index, row in enumerate(all_rows):
    book_name = str(row[1]).strip() if row[1] is not None else ""
    author = str(row[2]).strip() if row[2] is not None else ""
    score = row[3]
    publisher = str(row[4]).strip() if row[4] is not None else ""
    publish_time = str(row[5]).strip() if row[5] is not None else ""
    comment_cnt_raw = str(row[6]).strip() if row[6] is not None else ""
    price = str(row[7]).strip() if row[7] is not None else ""

    c3 = re.search(r"(\d{4})", publish_time) is None
    c4 = bool(re.search(r"[\u4e00-\u9fff]", publish_time))
    c5 = bool(re.search(r"[\u4e00-\u9fff]", re.sub("元","",price)))
    c6 = bool(re.search(r"[\u4e00-\u9fff]", comment_cnt_raw))
    c7 = book_name == ""
    c8 = author == ""
    c9 = (score is None) or score <= 0 or score > 10
    c10 = (re.fullmatch(r"\d+", comment_cnt_raw) is None) or (int(comment_cnt_raw) <= 0)

    if c3 or c4 or c5 or c6 or c7 or c8 or c9 or c10:
        continue

    pub_year = None
    m_year = re.search(r"(\d{4})", publish_time)
    if m_year:
        pub_year = int(m_year.group(1))

    price_num = None
    m_price = re.search(r"(\d+\.?\d*)", price)
    if m_price:
        price_num = float(m_price.group(1))

    one_row = (book_name, author, score, publisher, publish_time, row[6], price, pub_year, price_num)
    try:
        cur.execute(insert_sql, one_row)
        success += 1
    except Exception as err:
        bad_items.append((index, one_row, str(err)))

conn.commit()

print(f"\n✅成功写入 {success} 条")
if len(bad_items) > 0:
    print(f"❌有 {len(bad_items)} 条插入失败：")
    for idx,data,errmsg in bad_items:
        print(f"行号{idx} 数据：{data} → 错误：{errmsg}")

cur.close()
conn.close()
