from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = ['item_name', 'item_description','item_quantity','date_created','updated_at']
        
          