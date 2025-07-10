# inventory/management/commands/import_labs.py

import csv
import re
from django.core.management.base import BaseCommand
from inventory.models import Laboratorio, LaboratorioType

class Command(BaseCommand):
    help = 'Importa laboratórios, combinando nome e tipo para criar um nome único.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV.')

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        self.stdout.write(self.style.SUCCESS(f'Iniciando importação do arquivo: {file_path}'))

        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Lógica para tipo e coordenadas (continua a mesma)
                lab_type_obj = None
                tipo_str = row.get('Tipo', '').strip()
                if tipo_str:
                    lab_type_obj, _ = LaboratorioType.objects.get_or_create(name=tipo_str)

                lat, lng = None, None
                coordenadas_str = row.get('Coordenadas', '').strip()
                if coordenadas_str:
                    numeros = re.findall(r'-?\d+\.\d+', coordenadas_str)
                    if len(numeros) == 2:
                        try:
                            lat, lng = float(numeros[0]), float(numeros[1])
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Coordenadas inválidas para o lab: {row.get('Nome', 'N/A')}"))
                
                # --- INÍCIO DA NOVA LÓGICA DE NOME COMBINADO ---
                
                nome_original = row.get('Nome', '').strip()
                
                # Cria o nome combinado apenas se o tipo existir
                if tipo_str:
                    nome_combinado = f"{nome_original} - {tipo_str}"
                else:
                    nome_combinado = nome_original

                # Define os dados que serão criados ou atualizados
                defaults_data = {
                    'endereco': row.get('Endereco', ''),
                    'numero': row.get('Numero', ''),
                    'uf': row.get('UF', ''),
                    'telefone': row.get('Telefone', ''),
                    'latitude': lat,
                    'longitude': lng,
                    'lab_type': lab_type_obj,
                    # Adicionamos o nome original aqui para o caso de uma atualização
                    # não sobrescrever o nome combinado.
                    'name': nome_combinado
                }

                # O Django agora usa o NOME COMBINADO para encontrar o registro
                lab, created = Laboratorio.objects.update_or_create(
                    name=nome_combinado,
                    defaults=defaults_data
                )
                # --- FIM DA NOVA LÓGICA ---

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Laboratório "{lab.name}" criado com sucesso.'))
                else:
                    self.stdout.write(self.style.NOTICE(f'Laboratório "{lab.name}" atualizado.'))

        self.stdout.write(self.style.SUCCESS('Importação concluída!'))