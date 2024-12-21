# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import UserProfileCreationForm, EmployeeForm
from .models import Employee
from django.contrib.auth.decorators import login_required, user_passes_test


def register(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 自动为新用户创建 Employee 实例
            if not Employee.objects.filter(user=user).exists():
                Employee.objects.create(user=user, name=user.username)  # 你可以根据实际需求初始化其他字段
            login(request, user)  # 自动登录
            if user.role == 'admin':
                return redirect('user:admin_dashboard')
            else:
                return redirect('user:employee_dashboard')
    else:
        form = UserProfileCreationForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('user:admin_dashboard')
                else:
                    return redirect('user:employee_dashboard')
            else:
                # 登录失败的处理
                return render(request, 'user/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user:login')

from django.contrib.auth.decorators import login_required, user_passes_test

# 检查用户是否是管理员
def is_admin(user):
    return user.role == 'admin'

# 员工主页
@login_required
def employee_dashboard(request):
    return render(request, 'user/employee_dashboard.html')

# 管理员主页
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'user/admin_dashboard.html')


@login_required
def employee_profile(request):
    # 获取当前登录的员工对象
    employee = request.user.employee_profile
    
    if request.method == 'POST':
        # 如果是POST请求，表示修改信息
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # 保存修改后的信息
            return redirect('user:employee_dashboard')  # 重定向回个人信息页面
    else:
        form = EmployeeForm(instance=employee)  # 获取当前员工的信息填充表单
    
    return render(request, 'employee/employee_profile.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def admin_employee_list(request):
    # 获取所有员工信息
    employees = Employee.objects.all()
    return render(request, 'employee/admin_employee_list.html', {'employees': employees})

@login_required
@user_passes_test(is_admin)
def admin_edit_employee(request, employee_id):
    # 编辑指定员工信息
    employee = Employee.objects.get(id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('user:admin_dashboard')
    else:
        form = EmployeeForm(instance=employee)
    
    return render(request, 'employee/admin_edit_employee.html', {'form': form, 'employee': employee})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    # 处理表单提交
    pass
