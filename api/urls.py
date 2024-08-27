from os import name
from django.urls import path, re_path, include
from django.utils.timezone import utc
from . import views
from rest_framework import routers

app_name = "api"

router =routers.DefaultRouter()

urlpatterns = [
    re_path(r'^auth$', views.LoginApiView.as_view()),
    re_path(r'^ligne-budgetaire$', views.ligneBudgetaire.as_view()),
    re_path(r'^operation-budgetaire$', views.OperationBugetaire.as_view()),
    re_path(r'^activite-budgetaire$', views.ActiviteBugetaire.as_view()),
    re_path(r'^transfert-budgetaire$', views.TransfertBugetaire.as_view()),
]