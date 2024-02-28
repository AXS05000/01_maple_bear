from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF
from .models import YEAR_CHOICES
from .models import Base, Contrato, Templates, AvaliacaoFDMP


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
            "data_de_recebimento_da_oferta": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date"}),
            "data_de_inicio_contrato": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date"}),
            "data_do_fim_contrato": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date"}),
            "cambio_data": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date"}),
            "data_de_assinatura": forms.DateInput(format='%Y-%m-%d', attrs={"type": "date"}),
        }
    def clean_cpf(self):
        cpf_original = self.cleaned_data.get("cpf")
        # Remove pontos e traço para validar apenas os dígitos
        cpf = cpf_original.replace(".", "").replace("-", "")
        if not self.validate_cpf(cpf):
            raise ValidationError("CPF inválido.")
        # Retorna o CPF original formatado
        return cpf_original

    @staticmethod
    def validate_cpf(cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        # Converte a string em uma lista de inteiros
        numbers = [int(digit) for digit in cpf]
        # Validação do primeiro dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:9], range(10, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False
        # Validação do segundo dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:10], range(11, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False
        return True
    


class FDMPForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoFDMP
        fields = "__all__"

    def clean_cpf(self):
        cpf_original = self.cleaned_data.get("cpf")
        # Remove pontos e traço para validar apenas os dígitos
        cpf = cpf_original.replace(".", "").replace("-", "")
        if not self.validate_cpf(cpf):
            raise ValidationError("CPF inválido.")
        # Retorna o CPF original formatado
        return cpf_original

    @staticmethod
    def validate_cpf(cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        # Converte a string em uma lista de inteiros
        numbers = [int(digit) for digit in cpf]
        # Validação do primeiro dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:9], range(10, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False
        # Validação do segundo dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:10], range(11, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False
        return True
    


class FDMPFormEdit(forms.ModelForm):
    class Meta:
        model = AvaliacaoFDMP
        fields = "__all__"
        exclude = ('cnpj', 'razao_social',) 

    def clean_cpf(self):
        cpf_original = self.cleaned_data.get("cpf")
        # Remove pontos e traço para validar apenas os dígitos
        cpf = cpf_original.replace(".", "").replace("-", "")
        if not self.validate_cpf(cpf):
            raise ValidationError("CPF inválido.")
        # Retorna o CPF original formatado
        return cpf_original

    @staticmethod
    def validate_cpf(cpf):
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        # Converte a string em uma lista de inteiros
        numbers = [int(digit) for digit in cpf]
        # Validação do primeiro dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:9], range(10, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False
        # Validação do segundo dígito verificador
        sum_of_products = sum([a * b for a, b in zip(numbers[0:10], range(11, 1, -1))])
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False
        return True