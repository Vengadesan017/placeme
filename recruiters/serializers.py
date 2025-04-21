from rest_framework import serializers
from recruiters.models import Positions, HireRequests
from django.utils.timesince import timesince

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = [
            'position_id',
            'position_title',
            'position_code',
            'description',
        ]

class NestedPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positions
        fields = ['position_title', 'position_code', 'description']

class HireRequestSerializer(serializers.ModelSerializer):
    position = NestedPositionSerializer()

    class Meta:
        model = HireRequests
        fields = [
            'hire_request_id',
            'hire_request_code',
            'created_at',
            'deadline',
            'is_open',
            'position'
        ]
