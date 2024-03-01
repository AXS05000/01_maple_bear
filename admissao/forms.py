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
    



class CNPJForm(forms.Form):
    cnpj = forms.CharField(max_length=18)

    widgets = {
            "cnpj": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CNPJ",
                }
            ),
        }
    



class FDMPFormEdit(forms.ModelForm):
    class Meta:
        model = AvaliacaoFDMP
        fields = "__all__"
        exclude = ('cnpj', 'razao_social', 'bloqueado_para_edicao')

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

    def clean(self):
        cleaned_data = super().clean()

        pairs = [
            ('bear_care_qtd', 'bear_care_vm'),
            ('toddler_qtd', 'toddler_vm'),
            ('nursery_qtd', 'nursery_vm'),
            ('junior_kindergarten_qtd', 'junior_kindergarten_vm'),
            ('senior_kindergarten_qtd', 'senior_kindergarten_vm'),
            ('year_1_qtd', 'year_1_vm'),
            ('year_2_qtd', 'year_2_vm'),
            ('year_3_qtd', 'year_3_vm'),
            ('year_4_qtd', 'year_4_vm'),
            ('year_5_qtd', 'year_5_vm'),
            ('year_6_qtd', 'year_6_vm'),
            ('year_7_qtd', 'year_7_vm'),
            ('year_8_qtd', 'year_8_vm'),
            ('year_9_qtd', 'year_9_vm'),
            ('year_10_qtd', 'year_10_vm'),
            ('year_11_qtd', 'year_11_vm'),
            ('year_12_qtd', 'year_12_vm'),
        ]

        for qtd_field, vm_field in pairs:
            qtd = cleaned_data.get(qtd_field)
            vm = cleaned_data.get(vm_field)

            # Verifica se o valor médio está preenchido enquanto a quantidade é zero
            if vm and vm != 0 and (qtd is None or qtd == 0):
                self.add_error(qtd_field, ValidationError(
                    "Este campo não pode ser zero se o valor médio da mensalidade for diferente de zero."
                ))

            # Verifica se a quantidade está preenchida enquanto o valor médio é zero
            if qtd and qtd != 0 and (vm is None or vm == 0):
                self.add_error(vm_field, ValidationError(
                    "Este campo não pode ser zero se a quantidade de alunos for diferente de zero."
                ))

        return cleaned_data