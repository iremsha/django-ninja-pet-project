from django.urls import path
from .views import AllView, PingView, AddView, SubstractView, StatusView

urlpatterns = [
    path('all/<int:offset>/<int:amount>/', AllView.as_view()),
    path('ping/', PingView.as_view()),
    path('add/', AddView.as_view()),
    path('substract/', SubstractView.as_view()),
    path('status/', StatusView.as_view()),
]
