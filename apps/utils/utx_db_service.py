# ./apps/utils/utx_db_service.py

import os

from django.apps import apps
from django.db import connection
from models.order import Order
from models.orderbook import OrderBook
from models.ticker import Ticker
from models.trade import Trade


class UtxDBService:
    def __init__(self):
        self.models_directory = os.environ["UTX_DATA_MODELS"]
        self.django_to_pg_type_mapping = {
            "AutoField": "SERIAL",
            "BigAutoField": "BIGSERIAL",
            "BooleanField": "BOOLEAN",
            "CharField": "VARCHAR",
            "DateField": "DATE",
            "DateTimeField": "TIMESTAMP",
            "DecimalField": "NUMERIC",
            "DurationField": "INTERVAL",
            "FileField": "VARCHAR",
            "FloatField": "DOUBLE PRECISION",
            "IntegerField": "INTEGER",
            "BigIntegerField": "BIGINT",
            "NullBooleanField": "BOOLEAN",
            "PositiveIntegerField": "INTEGER",
            "PositiveSmallIntegerField": "SMALLINT",
            "SlugField": "VARCHAR",
            "SmallAutoField": "SMALLSERIAL",
            "SmallIntegerField": "SMALLINT",
            "TextField": "TEXT",
            "TimeField": "TIME",
            "UUIDField": "UUID",
            # Add more mappings as needed
        }

    def get_models(self):
        models = []
        for root, dirs, files in os.walk(self.models_directory):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    model_name = file[:-3]
                    models.append(model_name)
        return models

    def extract_model_fields(self, model_name):
        model_module = apps.get_model("data", model_name)
        fields = [
            (field.name, field.get_internal_type())
            for field in model_module._meta.get_fields()
        ]
        return model_name, fields

    def map_django_to_pg_type(self, django_type):
        return self.django_to_pg_type_mapping.get(django_type, django_type)

    def create_model_table(self, model_name, fields):
        pg_fields = [
            (name, self.map_django_to_pg_type(data_type)) for name, data_type in fields
        ]
        fields_str = ", ".join([f"{name} {data_type}" for name, data_type in pg_fields])
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS data_{model_name} ({fields_str})"
            )

    def create_models_tables(self):
        models = self.get_models()
        for model_name in models:
            model_name, fields = self.extract_model_fields(model_name)
            self.create_model_table(model_name, fields)
