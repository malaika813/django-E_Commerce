from . import views
from django.urls import path


urlpatterns = [
    path('recommend/', views.career_recommendation, name='recommendations'),
     path("chatbot/", views.chat_page, name="chat_page"),
    path("chat-api/", views.chat_api, name="chat_api"),
]