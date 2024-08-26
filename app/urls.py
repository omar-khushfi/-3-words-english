from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView,LogoutView
from . import views
urlpatterns = [
   path('',views.enter_words.as_view(),name="enter-words"),
   path('exam/',views.exam.as_view(),name="exam"),
   path('delete-word/<int:pk>',views.delete_word,name="delete-word"),
   path('words/', views.WordListView.as_view(), name='word-list'),
    
   
   
   
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signin/',views.Register.as_view(),name='signin'),
]
