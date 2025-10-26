from django.urls import path
from core.views import index

app_name = "glasses"

urlpatterns = [
    path("glasses/", index)
]