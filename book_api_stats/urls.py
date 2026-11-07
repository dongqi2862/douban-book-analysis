from django.urls import path
from . import views

urlpatterns = [
    path('api/score_all/', views.score_all, name='score_all'),
    path('api/country_count/', views.country_count, name='country_count'),
    path('api/hot_book/', views.hot_book, name='hot_book'),
    path('api/year_count/', views.year_count, name='year_count'),
    path('api/score_dist/', views.score_dist, name='score_dist'),
]
