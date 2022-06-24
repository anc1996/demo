from django.conf.urls import url
from ads import views

urlpatterns = [
    url(r'^$',views.AdsView.as_view()),
]