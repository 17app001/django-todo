from django.shortcuts import render
from .models import Todo


# Create your views here.
def todolist(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})
