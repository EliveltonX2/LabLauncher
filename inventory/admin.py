# inventory/admin.py

from django.contrib import admin
from .models import Laboratorio, EquipmentType, EquipmentInstance, LaboratorioType


@admin.register(LaboratorioType)
class LaboratorioTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


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
    list_display = ('name', 'lab_type', 'status', 'created_at')
    list_filter = ('status', 'lab_type')
    search_fields = ('name', 'description')
    filter_horizontal = ('inspectors',)

    fieldsets = (
        ('Informações Principais', {
            'fields': ('name', 'description', 'lab_type', 'status')
        }),
        ('Localização', {
            'fields': ('endereco', 'numero', 'uf', 'latitude', 'longitude')
        }),
        ('Contato e Responsáveis', {
            'fields': ('telefone', 'inspectors')
        }),
    )

    

@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lab', 'status')
    list_filter = ('status', 'lab', 'equipment_type')
    search_fields = ('serial_number', 'notes')