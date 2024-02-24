from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF
from .models import YEAR_CHOICES
from .models import Base, Contrato, Templates


class TemplateSelectForm(forms.Form):
    template = forms.ModelChoiceField(queryset=Templates.objects.all())


class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=200)
    file = forms.FileField()
    ano_vigencia = forms.ChoiceField(choices=[("", "----------")] + YEAR_CHOICES)


# class Admissao(forms.ModelForm):
#     class Meta:
#         model = Contrato
#         fields = [
#             "name",
#             "cpf",
#             "rg",
#             "orgao_emissor_rg",
#             "uf_rg",
#             "data_emissao_rg",
#             "n_ctps",
#             "serie",
#             "uf_ctps",
#             "data_emissao_ctps",
#             "endereco",
#             "cep",
#             "celular",
#             "email",
#         ]
#         requireds = [
#             "name",
#             "cpf",
#             "rg",
#             "orgao_emissor_rg",
#             "uf_rg",
#             "data_emissao_rg",
#             "n_ctps",
#             "serie",
#             "uf_ctps",
#             "data_emissao_ctps",
#             "endereco",
#             "cep",
#             "celular",
#             "email",
#         ]

#     def clean_cpf(self):
#         cpf = self.cleaned_data.get("cpf")
#         cpf_validator = CPF()

#         if cpf and not cpf_validator.validate(cpf):
#             raise ValidationError("CPF inválido")

#         return cpf


class AdmissaoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = "__all__"
        widgets = {
            "data_de_recebimento_da_oferta": forms.DateInput(attrs={"type": "date"}),
            "data_de_inicio_contrato": forms.DateInput(attrs={"type": "date"}),
            "data_do_fim_contrato": forms.DateInput(attrs={"type": "date"}),
            "cambio_data": forms.DateInput(attrs={"type": "date"}),
            "data_de_assinatura": forms.DateInput(attrs={"type": "date"}),
        }
