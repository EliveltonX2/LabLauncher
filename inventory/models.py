# inventory/models.py
import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
# Importamos nosso storage S3 para aplicar nos FileFields
from config.storages import S3MediaStorage

# Lógica de seleção de storage que já usamos
if os.getenv('USE_S3') == 'TRUE':
    storage_para_usar = S3MediaStorage()
else:
    storage_para_usar = FileSystemStorage()


class LaboratorioType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nome do Tipo")
    description = models.TextField(blank=True, verbose_name="Descrição")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Laboratório"
        verbose_name_plural = "Tipos de Laboratório"


class Laboratorio(models.Model):

    STATUS_CHOICES = (
        ('ok', 'OK'),
        ('projeto', 'Em Projeto'),
        ('instalacao', 'Em Instalação'),
        ('manutencao', 'Em Manutenção'),
    )

    name = models.CharField(max_length=200, verbose_name="Nome do Laboratório")
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço")
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número")
    uf = models.CharField(max_length=2, blank=True, verbose_name="UF")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    description = models.TextField(blank=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='projeto', verbose_name="Status")

    lab_type = models.ForeignKey(
        LaboratorioType, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="laboratorios",
        verbose_name="Tipo de Laboratório"
    )

    # Relação Muitos-para-Muitos com os usuários que são inspetores deste laboratório
    inspectors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="inspected_labs",
        # Ajuda a filtrar no admin, mostrando apenas usuários que são staff
        limit_choices_to={'is_staff': True} 
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Retorna a URL para a página de detalhes deste laboratório
        return reverse('inventory:lab-detail', kwargs={'pk': self.pk})


class EquipmentType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Tipo de Equipamento")
    brand = models.CharField(max_length=100, blank=True, verbose_name="Marca")
    description = models.TextField(blank=True, verbose_name="Descrição")
    # Manual, especificações, etc.
    technical_manual = models.FileField(
        upload_to='equipment_manuals/', 
        storage=storage_para_usar, 
        blank=True, null=True,
        verbose_name="Manual Técnico"
    )

    def __str__(self):
        return f"{self.name} ({self.brand})"

class EquipmentInstance(models.Model):
    STATUS_CHOICES = (
        ('operacional', 'Operacional'),
        ('manutencao', 'Em Manutenção'),
        ('desativado', 'Desativado'),
    )
    # A qual tipo de equipamento esta instância pertence
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.CASCADE, related_name="instances")
    # Em qual laboratório esta instância física está
    lab = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name="equipments")
    serial_number = models.CharField(max_length=100, blank=True, verbose_name="Número de Série")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operacional')
    notes = models.TextField(blank=True, verbose_name="Notas de Manutenção")

    def __str__(self):
        return f"{self.equipment_type.name} - S/N: {self.serial_number or 'N/A'}"