from django.db import models


class Fault(models.Model):
    issuer = models.IntegerField()
    phone_number = models.IntegerField()
    date_time = models.CharField(max_length=20)
    topic = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    object_number = models.IntegerField()
    status = models.IntegerField()
    handler = models.CharField(max_length=20)
    priority = models.IntegerField()

    def get_fields(self):
        all_fields = []

        for field in Fault._meta.fields:
            all_fields.append(field)

        return [(field.name, field.value_to_string(self)) for field in all_fields]

    def __str__(self):
        return self.topic