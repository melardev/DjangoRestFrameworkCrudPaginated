from django.conf.urls import url

from todos.views import TodoListCreateView, TodoDetailsView

app_name = 'todos'
urlpatterns = [
    url(r'(?P<pk>([0-9])+)$', TodoDetailsView.as_view(), name='by_id'),
    url(r'$', TodoListCreateView.as_view(), name='todo-list'),

]
