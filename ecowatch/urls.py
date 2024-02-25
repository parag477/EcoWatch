from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('getdata/', views.getdata, name='getdata'),
    path('contact/', views.contact, name='contact'),
    path('topicsd/', views.topicsd, name='topicsd'),
    path('topicsl/', views.topicsl, name='topicsl'),
    path('details/', views.details, name='details'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
