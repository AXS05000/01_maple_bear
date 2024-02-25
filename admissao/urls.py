from django.urls import path

from . import views
from .views import ContratoSearchView, FormCandidatoCreateView, CandidatoUpdateView

urlpatterns = [
    path("upload_template/", views.upload_template, name="upload_template"),
    path("busca_candidato/", ContratoSearchView.as_view(), name="busca_candidato"),
    path("form_candidato/", FormCandidatoCreateView.as_view(), name="form_candidato"),
    path("editar/<int:pk>/", views.select_contract_id, name="edit_candidato"),
]
