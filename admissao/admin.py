from django.contrib import admin

from .models import Templates, Contrato, AvaliacaoFDMP

# Register your models here.
admin.site.register(Templates)

admin.site.register(Contrato)

admin.site.register(AvaliacaoFDMP)
