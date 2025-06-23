# inventory/models.py
import os
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Importamos nosso storage S3 para aplicar nos FileFields
from config.storages import S3MediaStorage

# Lógica de seleção de storage que já usamos
if os.getenv('USE_S3') == 'TRUE':
    storage_para_usar = S3MediaStorage()
else:
    storage_para_usar = FileSystemStorage()

class Laboratorio(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Laboratório")
    description = models.TextField(blank=True, verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

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