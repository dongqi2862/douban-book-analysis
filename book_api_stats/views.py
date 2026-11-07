from .models import Book
from django.db import connection
from django.http import JsonResponse

# 1.整体评分：平均分、最高分、最低分
def score_all(request):
    with connection.cursor() as cur:
        cur.execute("SELECT AVG(score) AS avg_score,MAX(score) AS max_score,MIN(score) AS min_score FROM final_book;")
        res = cur.fetchone()
    return JsonResponse({"avg_score":res[0],"max_score":res[1],"min_score":res[2]}, json_dumps_params={'ensure_ascii':False})

# 2.不同国家作者图书数量
def country_count(request):
    with connection.cursor() as cur:
        cur.execute("SELECT author_country,COUNT(*) AS book_count FROM final_book GROUP BY author_country ORDER BY book_count DESC;")
        rows = cur.fetchall()
        data = [{"country":r[0],"book_count":r[1]} for r in rows]
    return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii':False})

#3.评论数TOP10热门图书
def hot_book(request):
    with connection.cursor() as cur:
        cur.execute("SELECT book_name,author,score,comment_count FROM final_book ORDER BY comment_count DESC LIMIT 10;")
        rows = cur.fetchall()
        data = [{"book_name":r[0],"author":r[1],"score":r[2],"comment_count":r[3]} for r in rows]
    return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii':False})

#4.按出版年份统计图书数量
def year_count(request):
    with connection.cursor() as cur:
        cur.execute("SELECT pub_year,COUNT(*) AS book_count FROM final_book GROUP BY pub_year ORDER BY pub_year;")
        rows = cur.fetchall()
        data = [{"year":r[0],"book_count":r[1]} for r in rows]
    return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii':False})

#5.评分分布统计
def score_dist(request):
    with connection.cursor() as cur:
        cur.execute("SELECT score,COUNT(*) AS count FROM final_book GROUP BY score ORDER BY score;")
        rows = cur.fetchall()
        data = [{"score":r[0],"count":r[1]} for r in rows]
    return JsonResponse({"data":data}, json_dumps_params={'ensure_ascii':False})
