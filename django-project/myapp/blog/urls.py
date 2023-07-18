from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("", views.View.as_view(), name='list'),
    path("write/", views.Write.as_view(), name='write'),
    path("detail/<int:pk>/", views.Detail.as_view(), name='detail'),
    path("detail/<int:pk>/edit/", views.Update.as_view(), name='edit'),
]

