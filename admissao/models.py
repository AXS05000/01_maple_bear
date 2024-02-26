from django.db import models
from usuarios.models import CustomUsuario
from num2words import num2words
from decimal import Decimal, ROUND_DOWN
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
    ano_vigencia = models.CharField(max_length=4, choices=YEAR_CHOICES)

    def __str__(self):
        return f"{self.name}"

def formatar_valor(valor):
    # Converte para Decimal para manter precisão
    valor_decimal = Decimal(valor)
    # Formata com separadores de milhar e duas casas decimais
    # Usando quantize para evitar arredondamento indesejado
    valor_formatado = valor_decimal.quantize(Decimal("1.00"), rounding=ROUND_DOWN)
    # Formata com o padrão brasileiro de milhar e decimal
    return "{:,.2f}".format(valor_formatado).replace(",", "X").replace(".", ",").replace("X", ".")


def numero_por_extenso(valor, moeda='real'):
    valor_inteiro = int(valor)
    centavos = int((valor - valor_inteiro) * 100)
    texto = num2words(valor_inteiro, lang='pt_BR')
    
    if moeda == 'dolar':
        texto += " dólares" if valor_inteiro > 1 else " dólar"
    else:
        texto += " reais" if valor_inteiro > 1 else " real"
    
    if centavos > 0:
        texto += " e " + num2words(centavos, lang='pt_BR')
        texto += " centavos"
    
    return texto.capitalize()


class Contrato(Base):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=20)
    nascionalidade = models.CharField(max_length=200)
    estado_civil = models.CharField(max_length=200, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField()
    data_de_recebimento_da_oferta = models.DateField(null=True, blank=True)
    uf_pretendido = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    dias_vigencia = models.IntegerField(null=True, blank=True)
    data_de_inicio_contrato = models.DateField(null=True, blank=True)
    data_do_fim_contrato = models.DateField(null=True, blank=True)
    taxa_inicial_franquia = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    cambio_valor = models.DecimalField(max_digits=25, decimal_places=2, null=True, blank=True)
    cambio_data = models.DateField(null=True, blank=True)
    data_de_assinatura = models.DateField(null=True, blank=True)
    outros = models.CharField(max_length=25000, null=True, blank=True)
    endereco = models.CharField(max_length=550)
    numero = models.CharField(max_length=250)
    complemento = models.CharField(max_length=250)
    bairro = models.CharField(max_length=250)
    cidade_endereco = models.CharField(max_length=250)
    uf_endereco = models.CharField(max_length=2, choices=STATE_CHOICES)
    cep = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.nome}"

    def get_field_values(self):
        dias_por_extenso = num2words(self.dias_vigencia, lang='pt_BR')
        valor_dolar_extenso = numero_por_extenso(self.taxa_inicial_franquia, 'dolar')
        total_pagamento = self.cambio_valor * self.taxa_inicial_franquia
        total_pagamento_formatado = formatar_valor(total_pagamento)
        total_pagamento_extenso = numero_por_extenso(total_pagamento, 'real')
        taxa_inicial_franquia_formatado = formatar_valor(self.taxa_inicial_franquia)
        cambio_valor_formatado = formatar_valor(self.cambio_valor)
        cambio_valor_extenso = numero_por_extenso(self.cambio_valor, 'real')
        
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
            "{dias_por_extenso}": dias_por_extenso,
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
            "{taxa_inicial_franquia}": taxa_inicial_franquia_formatado,
            "{valor_dolar_extenso}": valor_dolar_extenso,
            "{total_a_ser_pago}": total_pagamento_formatado,
            "{total_pagamento_extenso}": total_pagamento_extenso,
            "{cambio_valor}": cambio_valor_formatado,
            "{cambio_valor_extenso}": cambio_valor_extenso,
            "{cambio_data}": (
                self.cambio_data.strftime("%d/%m/%Y") if self.cambio_data else ""
            ),
            "{data_de_assinatura}": (
                self.data_de_assinatura.strftime("%d/%m/%Y")
                if self.data_de_assinatura
                else ""
            ),
            "{outros}": self.outros,
            "{endereco}": self.endereco,
            "{numero}": self.numero,
            "{complemento}": self.complemento,
            "{bairro}": self.bairro,
            "{cidade_endereco}": self.cidade_endereco,
            "{uf_endereco}": self.uf_endereco,
            "{cep}": self.cep,
        }
