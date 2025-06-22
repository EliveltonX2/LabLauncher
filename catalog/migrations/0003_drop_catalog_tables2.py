# catalog/migrations/0002_drop_catalog_tables.py (ou o nome que foi gerado)

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # A dependência deve ser o nome do seu arquivo de migração anterior
        ('catalog', '0001_initial'), 
    ]

    operations = [
        migrations.RunSQL(
            # Este comando SQL deleta todas as tabelas possíveis do app catalog, se elas existirem.
            # O CASCADE cuida de remover as "ligações" (foreign keys) sem causar erros.
            "DROP TABLE IF EXISTS catalog_part, catalog_project, catalog_partcategory, catalog_projectcategory, catalog_category CASCADE;",
            # A operação reversa não precisa fazer nada.
            "SELECT 1;"
        )
    ]