from bs4 import BeautifulSoup
import pymysql
import re

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="txy20060411",
    database="douban_book",
    charset="utf8mb4",
    use_unicode=True
)
cur = conn.cursor()

file_list = [
    "page1.html",
    "page2.html",
    "page3.html",
    "page4.html",
    "page5.html",
    "page6.html",
    "page7.html",
    "page8.html",
    "page9.html",
    "page10.html"
]

total_count = 0

for file_name in file_list:
    print(f"\n====正在解析文件：{file_name}====")
    with open(file_name,"r",encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html,"html.parser")
    books = soup.find_all("tr", class_="item")
    page_cnt = len(books)
    print(f"本页抓到图书：{page_cnt}")
    total_count += page_cnt

    for item in books:
        #书名
        book_name = item.find("div",class_="pl2").find("a")["title"]
        #作者/出版时间/出版社/价格 整行文本
        info_text = item.find("p",class_="pl").get_text(strip=True)
        #评分
        score = item.find("span",class_="rating_nums").get_text(strip=True)
        #评论人数
        comment_raw = item.find("span",class_="pl").get_text(strip=True)

        #提取评论数字
        num_list = re.findall(r'\d+', comment_raw)
        if num_list:
            comment_count = int(num_list[0])
        else:
            comment_count = 0

        #拆分作者、出版社、出版时间、价格
        parts = info_text.split("/")
        author = parts[0].strip()
        publisher = parts[-3].strip()
        publish_time = parts[-2].strip()
        price = parts[-1].strip() #最后一段就是价格

        sql = """
        INSERT INTO book_info(book_name,author,score,publisher,publish_time,price,comment_count)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql,(book_name, author, score, publisher, publish_time, price, comment_count))

conn.commit()
cur.close()
conn.close()
print(f"\n✅全部处理完成，一共解析 {total_count} 本书")
