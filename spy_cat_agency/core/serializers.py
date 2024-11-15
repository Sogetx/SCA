from rest_framework import serializers
from .models import SpyCat, Mission, Target

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'completed', 'mission']
        extra_kwargs = {'mission': {'required': False}}
        
    def validate(self, data):
        # Перевірка, чи завершена місія або таргет
        mission = data.get('mission')
        if mission and mission.completed:
            raise serializers.ValidationError("Cannot add or modify targets for a completed mission.")
        return data

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'spy_cat', 'status', 'completed', 'targets']
    
    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission