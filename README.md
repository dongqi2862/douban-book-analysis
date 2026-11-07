# 豆瓣图书数据分析系统

基于 Django + MySQL + ECharts 的豆瓣图书数据分析可视化系统。

## 项目简介
对豆瓣图书数据进行爬取、清洗、统计分析与可视化展示。后端提供统计接口，前端用 ECharts 渲染图表。

## 技术栈
- 后端：Django、PyMySQL、MySQL
- 前端：HTML / CSS / JavaScript、ECharts
- 数据采集：Python 爬虫

## 目录结构
| 目录/文件 | 说明 |
|---|---|
| douban_book_api | Django 项目配置 |
| book_api_stats | 数据统计接口 |
| static | 前端页面 |
| spider | 爬虫代码 |
| Dump20261015.sql | 数据库脚本 |
| manage.py | 启动入口 |

## 运行方式
1. 导入数据库：
   `mysql -u root -p douban_book < Dump20261015.sql`
2. 修改 `douban_book_api/settings.py` 中的数据库账号密码
3. 安装依赖：`pip install django pymysql`
4. 启动后端：`python manage.py runserver`
5. 浏览器访问：`http://127.0.0.1:8000/static/index.html`

## 接口说明
| 接口 | 说明 |
|---|---|
| /api/score_all/ | 整体评分统计 |
| /api/country_count/ | 各国作者图书数量 |
| /api/hot_book/ | 评论 TOP10 热门图书 |
| /api/year_count/ | 按出版年份统计 |
