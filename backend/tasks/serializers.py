from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    title=serializers.CharField()
    due_date=serializers.DateField(required=False, allow_null=True)
    estimated_hours=serializers.FloatField(required=False, default=1)
    importance=serializers.IntegerField(required=False, default=5)
    dependencies=serializers.ListField(child=serializers.IntegerField(), required=False, default=list)
