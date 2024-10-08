from django.urls import path
from apps.users.views import UsernameCountView, RegisterView, LoginView, LoginStateView, LogoutView
urlpatterns = [
    # 判断用户名是否重复
    path('count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('state/', LoginStateView.as_view()),
    path('logout/', LogoutView.as_view()),
]
