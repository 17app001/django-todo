from django.shortcuts import render,redirect
from .models import Todo
from .forms import TodoForm
from datetime import datetime


def delete_todo(request,id):
    message=""
    user=get_user(request)    
    todo=None  
    if not user:
         message="未登入"
    else:
        try:
            todo = Todo.objects.get(id=id,user=user)          
            if not todo:
                message="編號不正確"
            else:              
                todo.delete()
             
        except Exception as e:
            message="刪除錯誤!"
        

    return redirect("todolist")


def create_todo(request):
    message=""
    user=get_user(request)    
    todo,form=None,None  
    if not user:
         message="未登入"
    else:
        if request.method=="POST":
            form=TodoForm(request.POST)
            todo=form.save(commit=False)
            if todo.completed:
                todo.date_completed=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                todo.date_completed=None

            todo.user=user
            todo.save()
            message="新增成功!"
        else:
            form=TodoForm()

    return render(request, "todo/create-todo.html", {"message":message,"form":form})




def todo(request,id):    
    message=""
    user=get_user(request)    
    todo,form=None,None  
    if user:
        try:
            todo = Todo.objects.get(id=id,user=user)
            print(todo)
            if not todo:
                message="編號不正確"
            else:
                if request.method=="GET":
                    form=TodoForm(instance=todo)
                else:
                    form=TodoForm(requset.POST,instance=todo)
                    form.save()
                    message="更新成功!"

        except Exception as e:
            message="編號不正確"
    else:
        message="請先登入"
    return render(request, "todo/todo.html", {"todo": todo,"message":message,"form":form})



def get_user(request):
    user=request.user
    if user.is_authenticated:
        return user

    return None

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
