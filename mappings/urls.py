from django.urls import path
from .views import (
    MappingListCreateView,
    PatientMappingsView,
    MappingDeleteView
)

urlpatterns = [
    path('', MappingListCreateView.as_view()),
    path('patient/<int:patient_id>/', PatientMappingsView.as_view()),
    path('<int:pk>/', MappingDeleteView.as_view()),
]