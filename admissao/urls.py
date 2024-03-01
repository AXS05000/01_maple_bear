from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ContratoSearchView, AvaliacaoFDMPViewSet, FormCandidatoCreateView, CandidatoUpdateView, FormFDMPFormCreateView, EscolasSearchView, FormFDMPUpdateView, ExcelImportView, CNPJSearchView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'avaliacoes', AvaliacaoFDMPViewSet)

urlpatterns = [
    path("upload_template/", views.upload_template, name="upload_template"),
    path('fdmp/', CNPJSearchView.as_view(), name='buscar_cnpj'),
    path("form_fdmp/", FormFDMPFormCreateView.as_view(), name="form_fdmp"),
    path("form_fdmp_edit/<int:pk>/", FormFDMPUpdateView.as_view(), name="form_fdmp_edit"),
    path("busca_escolas/", EscolasSearchView.as_view(), name="busca_escolas"),
    path('importar_excel/', ExcelImportView.as_view(), name='importar_excel'),
    path("form_candidato/", FormCandidatoCreateView.as_view(), name="form_candidato"),
    path("busca_candidato/", ContratoSearchView.as_view(), name="busca_candidato"),
    path("candidato_edit/<int:pk>/", CandidatoUpdateView.as_view(), name="candidato_edit"),
    path("editar/<int:pk>/", views.select_contract_id, name="edit_candidato"),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
