from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from Entreprise.views import EseValidation, ImportOrgFonctView, CreateOrganFonct, ListOrganFonct, UpdateOrganFonct, DelOrganFonct, \
    CreatePieceRechange, CreatePrestations,ListPieceRechange, ListPrestations, DeletePieceRechange, DeletePrestations, UpdatePieceRechange, \
        UpdatePrestations
from django.conf import settings
from Compteur.views import CompteurCreate, AlertEpViewSet, ListAlertEp, ListCountEpCritiq
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf.urls.static import static
from Matroulant.views import VehiculeViewSet, AssurViewSet, VisitechViewSet, CartegriseViewSet, ImportEnginView


router = SimpleRouter()
router.register("engins", VehiculeViewSet, basename="engins")

engin_router = routers.NestedSimpleRouter(router, "engins", lookup='engin')

engin_router.register("assurance", AssurViewSet, basename='engin-assurance')
engin_router.register("visitech", VisitechViewSet, basename='engin-visite')
engin_router.register("cartegrise", CartegriseViewSet, basename='engin-cartegrise')
engin_router.register("compteur", CompteurCreate, basename='engin-compteur')


urlpatterns = [
    path('api/auth/', include('djoser.urls')),
        
    # Endpoints Djoser pour les tokens JWT (login, refresh)
    path('api/auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('abonnement', EseValidation.as_view(), name="validation"),

    # LIENS DE L'ORGANIGRAMME DE L'ENTREPRISE

    path('import-organigramme', ImportOrgFonctView.as_view(), name="import-organigramme"), 
    path('creer-organes', CreateOrganFonct.as_view(), name='creer-organes'),
    path('list-organigramme', ListOrganFonct.as_view(), name='list-organigramme'),
    path('delete-org-fonct/<str:pk>', DelOrganFonct.as_view(), name='delete-org-fonct'),
    path('update-org-fonct/<str:pk>', UpdateOrganFonct.as_view(), name='update-org-fonct'),

    # LIENS DES ENGINS DE L'ENTREPRISE

    path('import-engins', ImportEnginView.as_view(), name="import-engins"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),



    path('creer-prestations', CreatePrestations.as_view(), name='creer-prestations'),
    path('list-prestations', ListPrestations.as_view(), name='list-prestations'),
    path('delete-prestations/<str:pk>', DeletePrestations.as_view(), name='delete-prestations'),
    path('update-prestations/<str:pk>', UpdatePrestations.as_view(), name='update-prestations'),


    path('creer-piece', CreatePieceRechange.as_view(), name='creer-piece'),
    path('list-piece', ListPieceRechange.as_view(), name='list-piece'),
    path('delete-piece/<str:pk>', DeletePieceRechange.as_view(), name='delete-piece'),
    path('update-piece/<str:pk>', UpdatePieceRechange.as_view(), name='update-piece'),

    path("depassement-ep/", ListCountEpCritiq.as_view(), name="depassement-ep"),
    
    
    # path("dt-ep/", DTEpCreate.as_view(), name="dt-ep"),

    # path("list-dt-ep/", ListDTEp.as_view(), name="list-dt-ep"),

    # path('alerts-ep/', ListAlertEp.as_view(), name='alerts-ep'),

    # path('suivi-ep/', ListSuiviEp.as_view(), name='suivi-ep'),

    


] + router.urls + engin_router.urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

