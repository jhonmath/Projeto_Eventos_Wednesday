from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(AtividadeInscrita)
admin.site.register(AtividadeLazer)
admin.site.register(Evento)
admin.site.register(Cupom)
admin.site.register(Local)
admin.site.register(Instituicao)
admin.site.register(ApoioEvento)
admin.site.register(Pagamento)
admin.site.register(EspacoFisico)
admin.site.register(Responsavel)
admin.site.register(Trilha)