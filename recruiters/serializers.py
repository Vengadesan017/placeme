from rest_framework import serializers
from recruiters.models import Positions, HireRequests, Benefits, Locations
from job_seekers.models import Skills, SpecificationForEdu
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




# for create job post form server options
class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='location_id')
    name = serializers.ReadOnlyField(source='display_label')

    class Meta:
        model = Locations
        fields = ['id', 'name']


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='skill_id')
    name = serializers.CharField(source='skill')
    name = serializers.CharField(source='display_name')  
    
    class Meta:
        model = Skills
        fields = ['id', 'name']


class QualificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='specification_id')
    name = serializers.CharField(source='display_name')  

    class Meta:
        model = SpecificationForEdu
        fields = ['id', 'name']


class BenefitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='benefits_id')
    name = serializers.CharField(source='benefit')

    class Meta:
        model = Benefits
        fields = ['id', 'name']
