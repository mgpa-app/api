from django.urls import path, include

urlpatterns = [
    # ... vos autres endpoints de tenant ...

    # Endpoints Djoser pour la gestion des utilisateurs (inscription, profil, etc.)
    path('api/auth/', include('djoser.urls')),
    
    # Endpoints Djoser pour les tokens JWT (login, refresh)
    path('api/auth/', include('djoser.urls.jwt')),
]