from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_quiz, name='start_quiz'),
    path('question/<int:index>/', views.question_view, name='question_view'),
    path('result/', views.result_view, name='result_view'),
    path('save-feedback/', views.save_feedback, name='save_feedback'),
]