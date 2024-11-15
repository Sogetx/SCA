from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer
import requests
from spy_cat_agency.core import serializers

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            breed = serializer.validated_data['breed']
            # Check breed
            if not self.validate_breed(breed):
                raise ValidationError("Invalid breed.")
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def validate_breed(self, breed):
        response = requests.get(f"https://api.thecatapi.com/v1/breeds/search?q={breed}")
        return response.json() != []

    @action(detail=True, methods=['patch'])
    def update_salary(self, request, pk=None):
        cat = self.get_object()
        if 'salary' not in request.data:
            return Response({"error": "Salary field is required"}, status=400)
        
        try:
            salary = float(request.data['salary'])
            if salary < 0:
                raise ValueError("Salary must be a positive number.")
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        cat.salary = salary
        cat.save()
        return Response({"status": "Salary updated", "new_salary": cat.salary})
    
class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.spy_cat is not None:
            raise ValidationError("Cannot delete a mission that is already assigned to a cat.")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        try:
            spy_cat = SpyCat.objects.get(id=request.data['cat_id'])
        except SpyCat.DoesNotExist:
            raise ValidationError("Invalid cat ID.")
        mission.spy_cat = spy_cat
        mission.save()
        return Response({"status": "cat assigned"})

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        mission = self.get_object()
        if mission.completed:
            raise ValidationError("Mission is already completed.")
        mission.completed = True
        mission.save()
        return Response({"status": "mission completed"})

    @action(detail=True, methods=['patch'])
    def update_notes(self, request, pk=None):
        mission = self.get_object()
        target_id = request.data.get('target_id')
        try:
            target = mission.targets.get(id=target_id)
        except Target.DoesNotExist:
            raise ValidationError("Invalid target ID.")
        if mission.completed or target.completed:
            raise ValidationError("Cannot update notes for completed mission or target.")
        target.notes = request.data['notes']
        target.save()
        return Response({"status": "notes updated"})

    @action(detail=True, methods=['patch'])
    def update_targets(self, request, pk=None):
        mission = self.get_object()
        if mission.completed:
            raise ValidationError("Cannot update targets for a completed mission.")
        targets_data = request.data.get('targets', [])
        for target_data in targets_data:
            target_id = target_data.pop('id', None)
            if target_id:
                try:
                    target = mission.targets.get(id=target_id)
                except Target.DoesNotExist:
                    raise ValidationError(f"Target with ID {target_id} does not exist.")
                for attr, value in target_data.items():
                    setattr(target, attr, value)
                target.save()
        return Response({"status": "targets updated"})

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['patch'])
    def mark_completed(self, request, pk=None):
        target = self.get_object()
        if target.completed:
            raise ValidationError("Target is already completed.")
        target.completed = True
        target.save()
        return Response({"status": "target marked as completed"})

    @action(detail=True, methods=['patch'])
    def update_notes(self, request, pk=None):
        target = self.get_object()
        if target.completed or target.mission.completed:
            raise ValidationError("Cannot update notes for completed target or mission.")
        notes = request.data.get('notes')
        if not notes:
            raise ValidationError("Notes field is required.")
        target.notes = notes
        target.save()
        return Response({"status": "notes updated"})

