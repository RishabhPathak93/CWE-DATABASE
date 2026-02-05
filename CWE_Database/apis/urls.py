from django.urls import path
from .views import find_cwe_tables, get_cwe_details

urlpatterns = [
    path("cwe/find/", find_cwe_tables),
    path("cwe/details/", get_cwe_details),
]
