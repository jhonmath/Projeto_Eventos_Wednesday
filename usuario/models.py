from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumField
from core import models as core_models


class EstadoInscricao(Enum):
    NAO_PAGO = 0
    PAGO = 1


class Tipo_permissao(Enum):
    DEFAULT = 0
    DONO = 1
    COLABORADOR = 2


class UsuarioManage(BaseUserManager):
    def _create_user(self, email, senha, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatorio')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nomedeusuario = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def criar_evento(self, titulo, descricao, tipo_evento, data_inicio, data_fim):
        evento = core_models.Evento(titulo=titulo, descricao=descricao, tipo_evento=tipo_evento, dt_inicio=data_inicio, dt_fim=data_fim, administrador=self)
        evento.save()

    def listar_evento(self):
        return self.eventos_criados.all()

    USERNAME_FIELD = 'nomedeusuario'
    PASSWORD_FIELD = 'senha'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManage()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def get_short_name(self):
        return self.nomedeusuario


class Funcionario(models.Model):
    evento = models.ForeignKey('core.Evento', on_delete=models.CASCADE, related_name='equipe')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='equipe')
    tipo_permmissao = EnumField(Tipo_permissao, default=Tipo_permissao.COLABORADOR)

    def atualizar_pagamento(self, incricao, valor):
        incricao.pagamento.realizar_pagamento(gestor=self, valor_pagamento=valor)

    def criar_cupom(self, desconto, validade, evento):
        cupom = Cupom(desconto=desconto, validade=validade, evento=evento)
        cupom.save()

    def checkar_presenca_atividade(self, nome_atividade, inscricao):
        lista_atividades = inscricao.get_atividades()

        #for atividdade in lista_atividades:
        #    if nome_atividade == atividdade.titulo:
        #        atividdade


class Inscricao(models.Model):
    evento = models.ForeignKey('core.Evento', on_delete=models.CASCADE, related_name='inscricoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField()
    valor = models.DecimalField(max_digits=4, decimal_places=2)
    status = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)
    pagamento = models.ForeignKey('core.Pagamento', on_delete=models.CASCADE, related_name="inscricao")

    def adicionar_atividade(self, atividade):
        if atividade in self.evento.atividades:
            self.atividades.add(atividade)
            self.valor += atividade.valor
        else:
            raise Exception("atividade nao adicionada")

    def aplicar_cupom(self, cupom):
        if cupom.validade_cupom():
            self.valor -= self.valor*cupom.desconto
        else:
            raise Exception("Cupom nao e valido  ")

    def get_atividades(self):
        return self.item_inscricao.atividade


class Check_in(models.Model):
    hora = models.TimeField('hora', blank=True, null=False, default="00:00")
    data = models.DateField('Data de entrada', auto_now_add=True)
    gerente = models.ForeignKey('usuario.Funcionario', related_name='gerente', )
    checked = models.BooleanField(default=False)

    def atividade_checkada(self, atividade):
        lista_atividades = self.item_inscricao
        for atividade_inscrita in lista_atividades:
            if atividade_inscrita.atividade.titulo == atividade.titulo:
                self.checked = True

        return self.checked


class Item_Inscricao(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, related_name='item_inscricao')
    atividade = models.ForeignKey('core.AtividadeInscrita', on_delete=models.CASCADE, related_name='item_inscrisao')
    horario = models.TimeField()
    check_in = models.ForeignKey(Check_in, on_delete=models.CASCADE, related_name='item_inscricao')
