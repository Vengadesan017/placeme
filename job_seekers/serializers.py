from rest_framework import serializers
from recruiters.models import Jobs ,Companies, Locations
from django.utils.timesince import timesince

# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Locations
#         fields = ['location_id', 'location'] 
class JobsCardSerializer(serializers.ModelSerializer):
    # location_id = LocationSerializer(many=True)  #  Nested serializer for detailed output
    location_id = serializers.StringRelatedField(many=True)  #  Shows only location names
    qualifications = serializers.StringRelatedField(many=True) 
    skills = serializers.StringRelatedField(many=True) 
    company = serializers.StringRelatedField() 
    is_applied = serializers.BooleanField(read_only=True)
    is_saved = serializers.BooleanField(read_only=True)
    # time_since_posted = serializers.SerializerMethodField()
    class Meta:
        model = Jobs
        fields = (
        # 'job_id',
        'company', 
        'title',
        'slug',
        'location_id',
        'description',
        'employment_type',
        'is_fixed_shift',
        'is_rotational_shift',
        'is_day_shift',
        'is_night_shift',
        'is_onsite',
        'is_work_from_home',
        'is_hybrid',
        'is_applied',
        'is_saved',
        'skills', 
        'qualifications', 
        'min_experience', 
        'max_experience', 
        'salary',
        'salary_type',
        # 'get_time_since_posted',
        'last_date_to_apply',
        'refreshed_date',
        'opening_count',
        'views',
        'applied_count',
        ) 
    
    # def get_time_since_posted(self, obj):
    #     return timesince(obj.posted_date) + " ago"
    # def validate_salary(self, value):
    #     if value <=0:
    #         raise serializer.ValidationError(
    #             "Salary must be greater than zero"
    #             )
    #     return value   



class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['title']

# class LocationSerializer(serializers.ModelSerializer):
#     # id = serializers.IntegerField(source='location_id')
#     name = serializers.CharField(source='location')
#     name = serializers.CharField(source='display_name')  
    
#     class Meta:
#         model = Locations
#         fields = ['name']
        
# class LocationSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='location_id')
#     name = serializers.CharField(source='location')
#     name = serializers.CharField(source='display_name')  
    
#     class Meta:
#         model = Locations
#         fields = ['name']

class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='display_name')
    job_count = serializers.IntegerField()

    class Meta:
        model = Locations
        fields = ['name', 'job_count']