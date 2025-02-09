from django.urls import path
from . import views

urlpatterns= [
    path('login/', views.login_view, name='login'),
    path('', views.app_page, name="first"),
    path('manager/', views.db_manager_home, name="manager"),
    path('manager/addPlayers/', views.db_manager_add_player, name="managerAdd"),
    path('manager/addCoaches/', views.db_manager_add_coach, name="managerAdd"),
    path('manager/addJuries/', views.db_manager_add_jury, name="managerAdd"),
    path('manager/stadium/', views.db_manager_stadium, name="managerStadium"),
    path('coach/', views.coach_home, name="coach"),
    path('coach/deleteMatch', views.coach_delete_match, name="coachDelete"),
    path('coach/addMatch', views.coach_add_match, name="coachMatch"),
    path('coach/createSquad', views.coach_add_squad, name="coachSquad"),
    path('coach/stadium', views.coach_stadium, name="coachStadium"),
    path('jury/', views.jury_home, name= "jury"),
    path('jury/rate/', views.jury_rate, name= "juryRate"),
    path('player/', views.player_home, name="player"),
    path('logout/', views.log_out, name='logout')
]

