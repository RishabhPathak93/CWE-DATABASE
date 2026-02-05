from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apis.models import CWETableRegistry


def table_exists(table_name: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
            """,
            [table_name],
        )
        return cursor.fetchone() is not None


@api_view(["GET"])
def find_cwe_tables(request):
    cwe_id = request.GET.get("cwe_id")

    if not cwe_id:
        return Response({"error": "cwe_id is required"}, status=400)

    found_tables = []

    for entry in CWETableRegistry.objects.all():
        table = entry.table_name

        # ✅ Skip stale / missing tables
        if not table_exists(table):
            continue

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT 1 FROM "{table}" WHERE cwe_id = %s LIMIT 1',
                [cwe_id],
            )
            if cursor.fetchone():
                found_tables.append(table)

    return Response({
        "cwe_id": cwe_id,
        "tables": found_tables
    })


@api_view(["GET"])
def get_cwe_details(request):
    table = request.GET.get("table")
    cwe_id = request.GET.get("cwe_id")

    if not table or not cwe_id:
        return Response(
            {"error": "table and cwe_id are required"},
            status=400,
        )

    if not table_exists(table):
        return Response(
            {"error": f"Table '{table}' does not exist"},
            status=404,
        )

    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM "{table}" WHERE cwe_id = %s',
            [cwe_id],
        )
        row = cursor.fetchone()

        if not row:
            return Response(
                {"error": "CWE not found in this table"},
                status=404,
            )

        columns = [col[0] for col in cursor.description]
        return Response(dict(zip(columns, row)))
