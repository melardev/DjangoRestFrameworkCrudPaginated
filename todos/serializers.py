from rest_framework import serializers

from shared.serializers import PageMetaSerializer
from todos.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField(read_only=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'

    def get_description(self, instance):
        if self.context.get('include_details', False):
            return instance.description

    def to_representation(self, instance):
        response = super(TodoSerializer, self).to_representation(instance)
        if response.get('description') is None:
            response.pop('description')

        return response

    def create(self, validated_data):
        return Todo.objects.create(description=self.context.get('description', ''), **validated_data)


class TodoListSerializer(serializers.Serializer):
    success = True
    page_meta = serializers.SerializerMethodField()
    todos = serializers.SerializerMethodField()

    def get_page_meta(self, todos):
        return PageMetaSerializer(self.context['request'], self.context['paginator']).get_data()

    def get_todos(self, todos):
        return TodoSerializer(todos, many=True, context={'include_details': False}).data
