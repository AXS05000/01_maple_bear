from django.db import models
from usuarios.models import CustomUsuario


# Create your views here.
class Base(models.Model):
    data_de_criacao = models.DateField("Data de Criação", auto_now_add=True)
    data_de_modificacao = models.DateField("Data de Modificação", auto_now=True)
    usuario_modificacao = models.ForeignKey(
        CustomUsuario, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        abstract = True


YEAR_CHOICES = [
    ("2023", "2023"),
    ("2024", "2024"),
    ("2025", "2025"),
    ("2026", "2026"),
    ("2027", "2027"),
    ("2028", "2028"),
]

STATE_CHOICES = [
    ("AC", "Acre"),
    ("AL", "Alagoas"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("DF", "Distrito Federal"),
    ("ES", "Espírito Santo"),
    ("GO", "Goiás"),
    ("MA", "Maranhão"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("MG", "Minas Gerais"),
    ("PA", "Pará"),
    ("PB", "Paraíba"),
    ("PR", "Paraná"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RJ", "Rio de Janeiro"),
    ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("SC", "Santa Catarina"),
    ("SP", "São Paulo"),
    ("SE", "Sergipe"),
    ("TO", "Tocantins"),
]

MARITAL_STATUS_CHOICES = [
    ("solteiro", "Solteiro(a)"),
    ("casado", "Casado(a)"),
    ("divorciado", "Divorciado(a)"),
    ("viuvo", "Viúvo(a)"),
    ("separado", "Separado(a)"),
    ("uniao_estavel", "Em União Estável"),
]


class Templates(Base):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="contract_templates/")
    ano_vigencia = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Contrato(Base):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20)
    nascionalidade = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=200, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField()
    data_de_recebimento_da_oferta = models.DateField()
    uf_pretendido = models.CharField(max_length=2, choices=STATE_CHOICES)
    cidade = models.CharField(max_length=100)
    dias_vigencia = models.IntegerField()
    data_de_inicio_contrato = models.DateField()
    data_do_fim_contrato = models.DateField()
    taxa_inicial_franquia = models.DecimalField(max_digits=25, decimal_places=2)
    cambio_valor = models.DecimalField(max_digits=25, decimal_places=2)
    cambio_data = models.DateField()
    data_de_assinatura = models.DateField()
    outros = models.CharField(max_length=15000)

    def __str__(self):
        return f"{self.nome}"

    def get_field_values(self):
        return {
            "{nome}": self.nome,
            "{cpf}": self.cpf,
            "{rg}": self.rg,
            "{nascionalidade}": self.nascionalidade,
            "{estado_civil}": self.estado_civil,
            "{email}": self.email,
            "{data_de_recebimento_da_oferta}": (
                self.data_de_recebimento_da_oferta.strftime("%d/%m/%Y")
                if self.data_de_recebimento_da_oferta
                else ""
            ),
            "{uf_pretendido}": self.uf_pretendido,
            "{cidade}": self.cidade,
            "{dias_vigencia}": self.dias_vigencia,
            "{data_de_inicio_contrato}": (
                self.data_de_inicio_contrato.strftime("%d/%m/%Y")
                if self.data_de_inicio_contrato
                else ""
            ),
            "{data_do_fim_contrato}": (
                self.data_do_fim_contrato.strftime("%d/%m/%Y")
                if self.data_do_fim_contrato
                else ""
            ),
            "{taxa_inicial_franquia}": self.taxa_inicial_franquia,
            "{cambio_valor}": self.cambio_valor,
            "{cambio_data}": self.cambio_data,
            "{data_de_assinatura}": (
                self.data_de_assinatura.strftime("%d/%m/%Y")
                if self.data_de_assinatura
                else ""
            ),
            "{outros}": self.outros,
        }
