from django.shortcuts import render
from .models import Todo


def todo(request, id):
    message = ""
    user = request.user
    todo = None
    try:
        todo = Todo.objects.get(id=id, user=user)
    except Exception as e:
        print(e)
        message = "編號錯誤"

    return render(request, "todo/todo.html", {"todo": todo, "message": message})


# Create your views here.
def todolist(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})
