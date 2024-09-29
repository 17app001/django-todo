from django.shortcuts import render
from .models import Todo


# Create your views here.
def todolist(request):    
    message=""
    user=request.user
    todos=None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)
        if not todos:
            message="請先新增代辦事項"
    else:   
        message="請先登入或註冊"
 
    print(todos)
    return render(request, "todo/todolist.html", {"todos": todos,"message":message})
