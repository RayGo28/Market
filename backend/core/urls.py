from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('crypto/<str:symbol>/', views.crypto_detail, name='crypto_detail'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)