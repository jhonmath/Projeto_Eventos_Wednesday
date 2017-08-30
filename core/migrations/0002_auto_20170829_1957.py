# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 19:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='administrador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_criados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cupom',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Evento'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades', to='core.Evento'),
        ),
        migrations.AddField(
            model_name='apoioevento',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Evento'),
        ),
        migrations.AddField(
            model_name='apoioevento',
            name='instituicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Instituicao'),
        ),
    ]
