# redneuronal/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Endpoint principal (soporta múltiples formatos)
    path('prediccion/', views.predecir_componente, name='prediccion'),
    
    # Endpoint específico para URL
    path('prediccion-url/', views.predecir_desde_url, name='prediccion_url'),
    
    # Endpoints de información
    path('health/', views.health_check, name='health_check'),
    path('info/', views.info_modelo, name='info_modelo'),
]