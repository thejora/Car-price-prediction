from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=100, default='default_value', null=False)
    model = models.CharField(max_length=50,default='default_value', null=False)
    year = models.IntegerField(null=False)
    engine_capacity = models.DecimalField(max_digits=4,decimal_places=1, null=False)
    horses = models.IntegerField(null=False)
    fuel = models.CharField(max_length=10,default='default_value', null=False)
    transmission = models.CharField(max_length=10,default='default_value', null=False)
    gearbox = models.CharField(max_length=10, default='default_value',null=False)
    distance = models.DecimalField(max_digits=7, decimal_places=1, null=False)
    repair = models.IntegerField(default='0', null=True)
    docs_problems = models.IntegerField(default='0', null=True)
    id = models.IntegerField(primary_key=True, db_index=True)

