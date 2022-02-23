from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login_here,name="login_here"),
    path("register/",views.register_here,name="register_here"),
    path("register_site/",views.register_for_site,name="site"),
    path("login_site/",views.login_site,name="log_site"),
    #path("verify/",views.verification,name="verify"),
]