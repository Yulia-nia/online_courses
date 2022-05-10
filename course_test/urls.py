from django.urls import path
from . import views
from .views import GetQuestion, QuestionAnswer

urlpatterns = [
    path('', GetQuestion.as_view()),
    path('answer/', QuestionAnswer.as_view()),
]