from django.urls import path

from . import views
from .views import ContratoSearchView, FormCandidatoCreateView, CandidatoUpdateView, FormFDMPFormCreateView, EscolasSearchView, FormFDMPUpdateView

urlpatterns = [
    path("upload_template/", views.upload_template, name="upload_template"),
    path("form_fdmp/", FormFDMPFormCreateView.as_view(), name="form_fdmp"),
    path("form_fdmp_edit/<int:pk>/", FormFDMPUpdateView.as_view(), name="form_fdmp_edit"),
    path("busca_escolas/", EscolasSearchView.as_view(), name="busca_escolas"),
    path("form_candidato/", FormCandidatoCreateView.as_view(), name="form_candidato"),
    path("busca_candidato/", ContratoSearchView.as_view(), name="busca_candidato"),
    path("candidato_edit/<int:pk>/", CandidatoUpdateView.as_view(), name="candidato_edit"),
    path("editar/<int:pk>/", views.select_contract_id, name="edit_candidato"),
]
