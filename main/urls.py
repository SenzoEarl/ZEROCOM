from django.urls import path

from main import views
from main.views import *

app_name = 'hub'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post-list/', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/submit/', QuizSubmitView.as_view(), name='quiz_submit'),
    path('quizzes/<int:pk>/result/', QuizResultView.as_view(), name='quiz_result'),
    path('quizzes/<int:pk>/results/', QuizResultsListView.as_view(), name='quiz_results_list'),
    path('lottery/', LotteryList.as_view(), name='lottery_list'),
    path('<int:post_id>/share/', post_share, name='post_share'),
]