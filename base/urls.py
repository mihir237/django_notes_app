from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    path('home/', views.home, name='home'),
    path('lable/<str:pk>', views.note, name='note'),
    path('create-lable', views.createLable, name='create-lable'),
    path('note-details/<str:pk>', views.noteDetails, name='note-details'),
    path('note-delete/<str:pk>', views.deleteNote, name='delete-note'),
    path('update-note/<str:pk>', views.updateNote, name='update-note'),
]
