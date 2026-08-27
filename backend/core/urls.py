from django.urls import  include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"coins", views.Coins, basename='coins')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/',include(router.urls)),
    path('api/global/', views.get_global_data, name="global_data")
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)