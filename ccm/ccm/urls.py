from django.contrib import admin
from django.urls import path
from credd.views import signUp, login, spend_credit, pay_bill

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/", signUp),
    path("login/", login),
    path("spend/", spend_credit),
    path("pay/", pay_bill)
]
