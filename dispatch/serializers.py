from rest_framework import serializers
from .models import Dispatch

class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = ['item_name', 'item_description','item_quantity','date_created','updated_at', 'status']