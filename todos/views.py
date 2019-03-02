# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response

from shared.serializers import ErrorSerializer, SuccessSerializer
from todos.models import Todo
from todos.serializers import TodoListSerializer, TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TodoListSerializer
    queryset = Todo.objects.all()

    def get_queryset(self):
        if self.request.path.endswith('pending'):
            self.queryset = self.queryset.filter(completed=False)
        elif 'completed' in self.request.path:
            self.queryset = self.queryset.filter(completed=True)

        self.queryset = self.queryset.order_by('-created_at')
        return self.queryset

    def list(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        context['request'] = request
        page = self.paginate_queryset(self.get_queryset())
        context['paginator'] = self.paginator
        serialized_data = self.serializer_class(page, context=context).data
        return Response(serialized_data)

    def create(self, request, **kwargs):

        serializer_data = request.data
        serializer_context = {
            'include_details': True,
            'description': request.data['description']
        }

        serializer = TodoSerializer(data=serializer_data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {'success': True, 'full_messages': ['Todo Created successfully']}
        response.update(serializer.data)
        return Response(response, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        Todo.objects.all().delete()
        return Response(SuccessSerializer('All todos successfully').data)


class TodoDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def get_object(self):
        try:
            return Todo.objects.get(pk=self.kwargs[self.lookup_field])
        except Todo.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo is None:
            return Response(ErrorSerializer('Todo not Found').data)
        todo.title = request.data['title']
        todo.description = request.data['description']
        todo.completed = request.data['completed']
        todo.save()
        data = self.serializer_class(todo, context={'include_details': True}).data
        response = {'success': True, 'full_messages': ['Todo updated successfully']}
        response.update(data)
        return Response(response)

    def retrieve(self, request, *args, **kwargs):
        try:
            todo = Todo.objects.get(pk=kwargs['id'])
            response = {'success': True}
            data = self.serializer_class(todo, context={'include_details': True}).data
            response.update(data)
            return Response(response)
        except Todo.DoesNotExist:
            return Response(ErrorSerializer('Todo not Found').data)

    def delete(self, request, *args, **kwargs):
        try:
            todo = self.get_object()
            todo.delete()
            return Response(SuccessSerializer('Todo deleted successfully').data)
        except Todo.DoesNotExist:
            return Response(ErrorSerializer('Todo not Found').data)
