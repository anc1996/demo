from django.conf.urls  import url
from pay import views
urlpatterns = [
    url(r'^$',views.LoginView.as_view(),name='index'),
    url(r'^transfer/$',views.TransferView.as_view(),name='transfer'),
]