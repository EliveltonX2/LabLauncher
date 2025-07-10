# inventory/management/commands/import_labs.py

import csv
import re
from django.core.management.base import BaseCommand
# Importe também o LaboratorioType
from inventory.models import Laboratorio, LaboratorioType 

class Command(BaseCommand):
    help = 'Importa laboratórios a partir de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV a ser importado.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importação do arquivo: {file_path}'))

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # --- INÍCIO DA NOVA LÓGICA PARA O TIPO ---
                lab_type_obj = None
                tipo_str = row.get('Tipo', '').strip()
                if tipo_str:
                    # Procura por um tipo com esse nome. Se não existir, cria um novo.
                    lab_type_obj, created = LaboratorioType.objects.get_or_create(
                        name=tipo_str,
                        defaults={'name': tipo_str} # Garante que o nome seja salvo na criação
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Novo tipo de laboratório criado: "{tipo_str}"'))
                # --- FIM DA NOVA LÓGICA ---

                # Lógica para as coordenadas (continua a mesma)
                lat, lng = None, None
                coordenadas_str = row.get('Coordenadas', '').strip()
                if coordenadas_str:
                    numeros = re.findall(r'-?\d+\.\d+', coordenadas_str)
                    if len(numeros) == 2:
                        try:
                            lat = float(numeros[0])
                            lng = float(numeros[1])
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Não foi possível converter coordenadas para o lab: {row['Nome']}"))

                # Cria ou atualiza o laboratório, agora incluindo o lab_type
                lab, created = Laboratorio.objects.update_or_create(
                    name=row['Nome'],
                    defaults={
                        'endereco': row.get('Endereco', ''),
                        'numero': row.get('Numero', ''),
                        'uf': row.get('UF', ''),
                        'telefone': row.get('Telefone', ''),
                        'latitude': lat,
                        'longitude': lng,
                        'lab_type': lab_type_obj, # <-- ASSOCIA O TIPO AQUI
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Laboratório "{lab.name}" criado com sucesso.'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Laboratório "{lab.name}" atualizado.'))

        self.stdout.write(self.style.SUCCESS('Importação concluída!'))