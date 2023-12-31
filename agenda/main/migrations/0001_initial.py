# Generated by Django 4.2.7 on 2023-11-22 14:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cadastro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('nome', models.CharField(max_length=100, null=True)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('ie', models.CharField(max_length=20, null=True)),
                ('cidade', models.CharField(max_length=100, null=True)),
                ('bairro', models.CharField(max_length=100, null=True)),
                ('rua', models.CharField(max_length=100, null=True)),
                ('numero', models.IntegerField(null=True)),
                ('cep', models.CharField(max_length=100, null=True)),
                ('telefone', models.CharField(max_length=15, null=True)),
                ('whatsapp', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('celular', models.CharField(max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacoes', models.CharField(max_length=100, null=True)),
                ('cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cadastro')),
            ],
        ),
    ]
