from rest_framework import serializers 
from .models import table

class tableSerializer(serializers.ModelSerializer):
    class Meta:
        model = table
        fields = ('id','status')
    
    def create(self, validated_data):
        return table.objects.create(**validated_data)

