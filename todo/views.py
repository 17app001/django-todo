from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime


def delete_todo(request, id):
    user = request.user
    todo = None
    try:
        todo = Todo.objects.get(id=id, user=user)
        todo.delete()
    except Exception as e:
        print(e)

    return redirect("todolist")


# 新增代辦事項
def create_todo(request):
    message = ""
    user = request.user
    form = None
    if not user.is_authenticated:
        message = "請先登入"
    else:
        form = TodoForm()
        if request.method == "POST":
            try:
                print(request.POST)
                form = TodoForm(request.POST)
                todo = form.save(commit=False)
                todo.user = request.user
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                todo.date_completed = now if todo.completed else None

                todo.save()
                message = "提交成功!"
                return redirect("todolist")
            except Exception as e:
                print(e)
                message = "提交失敗!"

    return render(request, "todo/create-todo.html", {"form": form, "message": message})


# 檢視代辦事項
def todo(request, id):
    message = ""
    user = request.user
    todo = None

    try:
        todo = Todo.objects.get(id=id, user=user)
        form = TodoForm(instance=todo)
        if request.method == "POST":
            form = TodoForm(request.POST, instance=todo)
            todo = form.save(commit=False)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            todo.date_completed = now if todo.completed else None
            todo.save()
            message = "更新成功!"
            return redirect("todolist")
    except Exception as e:
        print(e)
        message = "編號錯誤"

    return render(
        request, "todo/todo.html", {"form": form, "todo": todo, "message": message}
    )


# Create your views here.
def todolist(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})


# Create your views here.
def completed(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/completed.html", {"todos": todos})
