from django.db import models

class CWETableRegistry(models.Model):
    """
    Stores metadata for each dynamically created CWE table
    """
    table_name = models.CharField(max_length=255, unique=True)
    source_file = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.table_name
