from django.conf.urls.defaults import *
import views

urlpatterns = patterns('myapp',
    url(r'^$', views.home, name="home"),
    url(r'^logout/$',
        views.logout_view,
        name="logout"),
    url(r'^login_form/$',
        views.login_form,
        name="login_form"),
)

