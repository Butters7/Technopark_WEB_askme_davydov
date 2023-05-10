from django.urls import path
from app import views

urlpatterns = [
    path('ask', views.ask, name="ask"),
    path('base', views.base, name="base"),
    path('hot', views.hot, name='hot'),
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('logout', views.log_out, name='logout'),
    path('question/<int:question_id>/', views.question, name="question"),
    path('settings', views.settings, name="settings"),
    path('signup', views.signup, name="signup"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
]
