
from django.contrib import admin
from django.urls import path, re_path, include
from Client.views import  ClientViewSet, ClientAbonneViewset, MontAbonViews
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter
from django.conf import settings
from Entreprise.views import EseValidation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static





router = SimpleRouter()
router.register('https://mgpa-api-jyeu.onrender.com/client', ClientViewSet) 
router.register('mgpa-api-jyeu.onrender.com/client', ClientViewSet)
router.register('https://onrender.com', ClientViewSet)
router.register('abonnement-ese', ClientAbonneViewset)
router.register('montant-abonnement', MontAbonViews)

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('abonnement', EseValidation.as_view(), name="validation"),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    
      
] + router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

