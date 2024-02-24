# Generated by Django 5.0.2 on 2024-02-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissao', '0002_alter_contrato_outros'),
    ]

    operations = [
        migrations.RenameField(
            model_name='templates',
            old_name='word',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='templates',
            old_name='nome',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='templates',
            name='ano_vigencia',
        ),
        migrations.AlterField(
            model_name='contrato',
            name='estado_civil',
            field=models.CharField(choices=[('solteiro', 'Solteiro(a)'), ('casado', 'Casado(a)'), ('divorciado', 'Divorciado(a)'), ('viuvo', 'Viúvo(a)'), ('separado', 'Separado(a)'), ('uniao_estavel', 'Em União Estável')], max_length=200),
        ),
    ]
