from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/<str:mode>/', views.game, name='game_mode'),
    path('check-answer/', views.check_answer, name='check_answer'),
]