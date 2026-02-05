import os
import re
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.apps import apps

CWETableRegistry = apps.get_model("apis", "CWETableRegistry")


def normalize_table_name(filename: str) -> str:
    """
    Convert file name into a safe SQL table name
    """
    name = os.path.splitext(filename)[0].lower()
    name = re.sub(r"[^a-z0-9_]+", "_", name)   # replace spaces & symbols
    name = re.sub(r"_+", "_", name).strip("_")
    return name


class Command(BaseCommand):
    help = "Load CWE CSV/XLSX files from apis/sheets into separate DB tables"

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sheets_dir = os.path.join(base_dir, "sheets")

        if not os.path.exists(sheets_dir):
            self.stderr.write("❌ sheets folder not found")
            return

        for file in os.listdir(sheets_dir):
            if not file.endswith((".csv", ".xlsx")):
                continue

            table_name = normalize_table_name(file)
            file_path = os.path.join(sheets_dir, file)

            self.stdout.write(f"📄 Processing {file} → table `{table_name}`")

            df = self.load_file(file_path)
            self.create_table(table_name)
            self.insert_data(table_name, df)
            self.register_table(table_name, file)

        self.stdout.write(self.style.SUCCESS("✅ CWE sheets loaded successfully"))

    def load_file(self, path):
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_excel(path)
        df.columns = [c.lower().strip() for c in df.columns]
        return df

    def create_table(self, table_name):
        with connection.cursor() as cursor:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id SERIAL PRIMARY KEY,
                    cwe_id TEXT,
                    title TEXT,
                    vulnerability_mapping TEXT,
                    abstraction TEXT,
                    description TEXT,
                    impact TEXT,
                    mitigation TEXT,
                    comments TEXT,
                    alternate_terms TEXT
                );
            """)

    @transaction.atomic
    def insert_data(self, table_name, df):
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {table_name}")

            for _, row in df.iterrows():
                cursor.execute(
                    f"""
                    INSERT INTO {table_name}
                    (cwe_id, title, vulnerability_mapping, abstraction,
                     description, impact, mitigation, comments, alternate_terms)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    [
                        row.get("id"),
                        row.get("title"),
                        row.get("vulnerability_mapping"),
                        row.get("abstraction"),
                        row.get("description"),
                        row.get("impact"),
                        row.get("mitigation"),
                        row.get("comments"),
                        row.get("alternate_terms"),
                    ],
                )

    def register_table(self, table_name, source_file):
        CWETableRegistry.objects.get_or_create(
            table_name=table_name,
            defaults={"source_file": source_file},
        )
