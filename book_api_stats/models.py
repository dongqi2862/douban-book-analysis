from django.db import models

# 映射已存在的豆瓣图书表final_book
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="书名")
    author = models.CharField(max_length=200, verbose_name="作者")
    rating = models.FloatField(verbose_name="评分")
    pub_year = models.IntegerField(verbose_name="出版年份")

    class Meta:
        db_table = "final_book"
        managed = False     # 不自动建表，表已经存在MySQL里
