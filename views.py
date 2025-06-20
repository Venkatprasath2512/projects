
from django.shortcuts  import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import todoo
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            return redirect('todopage')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')

def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html',{'error':'Email already taken'})

        my_user=User.objects.create_user(username=email,email=email,password=password)
        my_user.save()
        messages.success(request, 'User created successfully. Please login.')
        return redirect('login')
    return render(request,'signup.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def todo_view(request):
    if request.method == 'POST':
        task_content = request.POST.get('task')
        if task_content:
            todoo.objects.create(user=request.user, content=task_content)

    pending_tasks = todoo.objects.filter(user=request.user, completed=False)
    completed_tasks = todoo.objects.filter(user=request.user, completed=True)
    return render(request, 'todo.html', {'tasks': pending_tasks, 'completed_tasks': completed_tasks})


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(todoo, id=task_id, user=request.user)
    task.delete()
    return redirect('todopage')


@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(todoo, id=task_id, user=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('task')
        if new_content:
            task.content = new_content
            task.save()
            return redirect('todopage')

    return render(request, 'edit_task.html', {'task': task})


@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(todoo, id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect('todopage')

