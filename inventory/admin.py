# inventory/admin.py

from django.contrib import admin
from .models import Laboratorio, EquipmentType, EquipmentInstance

class EquipmentInstanceInline(admin.TabularInline):
    """Permite adicionar instâncias de equipamento diretamente na página do Tipo de Equipamento."""
    model = EquipmentInstance
    extra = 1 # Quantos formulários em branco mostrar

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand', 'description')
    inlines = [EquipmentInstanceInline] # Anexa a adição de instâncias aqui

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    # Melhora a interface de seleção de Muitos-para-Muitos para os inspetores
    filter_horizontal = ('inspectors',)

@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lab', 'status')
    list_filter = ('status', 'lab', 'equipment_type')
    search_fields = ('serial_number', 'notes')