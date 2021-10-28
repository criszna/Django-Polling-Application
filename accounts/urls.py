from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^Signup/$',views.signup_view,name='signup'),
    url(r'^Login/$',views.login_view,name="login"),
    url(r'^Logout/$',views.logout_view,name="logout"),

]