from django.urls import path
from . import views

urlpatterns = [
    path('', views.DispatchListAPIView.as_view(), name="dispatches"),
    path('<int:id>', views.DispatchDetailAPIView.as_view(), name="dispatch")
]