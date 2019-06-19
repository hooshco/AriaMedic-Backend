from rest_framework import serializers
from . import models

class StateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `State` instance, given the validated data.
        """
        return models.State.objects.create(**validated_data)

class MajorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    m_type = serializers.IntegerField()