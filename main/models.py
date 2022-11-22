from django.db import models


class Hospital(models.Model):
    client_name = models.CharField(max_length=255)
    client_org = models.CharField(max_length=255)
    number = models.IntegerField()
    sum = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField()
    service = models.CharField(max_length=255)

    class Meta:
        db_table = "hospital"
