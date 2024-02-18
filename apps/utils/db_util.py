import os

import pandas as pd
from django.apps import apps
from django.db import connection, models


class UtxDBService:
    def __init__(self):
        self.models_directory = os.environ.get("UTX_DATA_MODELS", "data")
        self.django_to_pg_type_mapping = self._default_django_to_pg_type_mapping()

    @staticmethod
    def _default_django_to_pg_type_mapping():
        """Provides default mapping from Django field types to PostgreSQL types."""
        return {
            models.AutoField: "SERIAL",
            models.BigAutoField: "BIGSERIAL",
            models.BooleanField: "BOOLEAN",
            models.CharField: "VARCHAR",
            models.DateField: "DATE",
            models.DateTimeField: "TIMESTAMP",
            models.DecimalField: "NUMERIC",
            models.DurationField: "INTERVAL",
            models.FileField: "VARCHAR",
            models.FloatField: "DOUBLE PRECISION",
            models.IntegerField: "INTEGER",
            models.BigIntegerField: "BIGINT",
            models.BooleanField: "BOOLEAN",  # NullBooleanField is deprecated
            models.PositiveIntegerField: "INTEGER",
            models.PositiveSmallIntegerField: "SMALLINT",
            models.SlugField: "VARCHAR",
            models.SmallAutoField: "SMALLSERIAL",
            models.SmallIntegerField: "SMALLINT",
            models.TextField: "TEXT",
            models.TimeField: "TIME",
            models.UUIDField: "UUID",
        }

    def get_models(self):
        """Fetches all models from the specified Django app, with error handling."""
        try:
            return apps.get_app_config(self.models_directory).get_models()
        except LookupError:
            raise LookupError(
                f"No installed app with label '{self.models_directory}'. Please check your UTX_DATA_MODELS environment variable and INSTALLED_APPS configuration."
            )

    def extract_model_fields(self, model):
        """Extracts field names and types from a given model, excluding reverse relations."""
        return [
            (field.name, type(field))
            for field in model._meta.get_fields()
            if not field.is_relation or field.one_to_many or field.one_to_one
        ]

    def map_django_to_pg_type(self, django_type):
        """Maps a Django field type to a PostgreSQL type."""
        return self.django_to_pg_type_mapping.get(
            django_type, "TEXT"
        )  # Default to TEXT for unmapped types

    def create_model_table(self, model):
        """Generates SQL for creating a table based on a Django model, using safe parameterized queries."""
        model_name = model._meta.model_name
        fields = self.extract_model_fields(model)
        pg_fields = [
            (name, self.map_django_to_pg_type(dtype)) for name, dtype in fields
        ]
        fields_str = ", ".join([f"{name} {data_type}" for name, data_type in pg_fields])

        # Using Django's ORM to execute raw SQL safely
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS data_{model_name} ({fields_str})"
            )

    def create_models_tables(self):
        """Creates PostgreSQL tables for all models in the specified Django app."""
        for model in self.get_models():
            self.create_model_table(model)
