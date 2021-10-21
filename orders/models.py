from django.db import models
from  authentication.models import User

# Create your models here.

class Order(models.Model):
    ITEM_OPTIONS=[
        ('Storage_and_Transport_Medical_Equipment', 'Storage_and_Transport_Medical_Equipment'),
        ('Durable_Medical_Equipment', 'Durable_Medical_Equipment'),
        ('Diagnostic_Medical_Equipment','Diagnostic_Medical_Equipment'),
        ('Electronic_Medical_Equipment','Electronic_Medical_Equipment'),
        ('Surgical_Medical_Equipment','Surgical_Medical_Equipment'),
        ('Acute_Care','Acute_Care'),
        ('Procedural_Medical_Equipment','Procedural_Medical_Equipment'),
        ('Others','Others')
    ]
    item_name=models.CharField(choices=ITEM_OPTIONS,max_length=255)
    item_description=models.CharField(max_length=255,blank=True)
    item_quantity=models.CharField(max_length=255,blank=True)
    location=models.CharField(max_length=255,blank=True)
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.owner)+'s order'
