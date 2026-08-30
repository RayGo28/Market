from django.urls import  include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView # type: ignore

router = routers.DefaultRouter()

router.register(r"coins", views.Coins, basename='coins')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/',include(router.urls)),
    path('api/global/', views.get_global_data, name="global_data"),
    
    
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    #path('api/market_analytics', views.market_analytics, name="market_analytics")
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)