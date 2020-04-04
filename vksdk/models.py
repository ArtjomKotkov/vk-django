from django.db import models
import pickle


class PickleField(models.BinaryField):
    def get_prep_value(self, value):
        return pickle.dumps(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return pickle.loads(value)

    def to_python(self, value):
        if value is None:
            return value
        return pickle.loads(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value).rows


class KeyBoards(models.Model):
    name = models.CharField(max_length=20, unique=True)
    keyboard = PickleField()


class Carousels(models.Model):
    name = models.CharField(max_length=20, unique=True)
    carousel = PickleField()
