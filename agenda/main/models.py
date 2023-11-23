from django.db import models
from django.utils import timezone

class Cadastro(models.Model):
    Id = models.AutoField(primary_key=True)
    data_criacao = models.DateTimeField(default=timezone.now)  
    nome = models.CharField(max_length=100, null=True)
    cnpj = models.CharField(max_length=14, null=True)
    cpf = models.CharField(max_length=14, null=True)
    ie = models.CharField(max_length=20, null=True)
    cidade = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=100, null=True)
    endereco = models.CharField(max_length=100, null=True)
    cep = models.CharField(max_length= 100, null=True)
    telefone = models.CharField(max_length=15, null=True) 
    whatsapp = models.CharField(max_length=15, null=True)
    email = models.EmailField()
    celular = models.CharField(max_length=15, null=True)
    def __str__(self):
        return self.nome

class Observacoes(models.Model):
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    observacoes = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.observacoes
