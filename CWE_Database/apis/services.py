#lets make the serializers for the above models
from rest_framework import serializers
from .models import CWEEntry
class CWEEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CWEEntry
        fields = ['cwe_id', 'table_name']
# This serializer will help in serializing and deserializing CWEEntry model instances.
# We can create additional serializers if needed for other functionalities.
