# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .forms import UserProfileCreationForm, EmployeeForm, LeaveRequestForm, AttendanceForm, AttendanceSettingsForm
from .models import Employee, LeaveRequest, Attendance, AttendanceSettings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Max

def register(request):
    if request.method == 'POST':
        form = UserProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 自动为新用户创建 Employee 实例
            if not Employee.objects.filter(user=user).exists():
                # 获取当前 Employee 表中的最大 id 值
                max_id = Employee.objects.aggregate(Max('id'))['id__max']
                new_id = max_id + 1 if max_id else 1  # 如果没有记录，则从 1 开始
                Employee.objects.create(id=new_id, user=user, name=user.username)  # 创建 Employee 实例
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
    # 获取查询参数
    query = request.GET.get('q', '')  # 默认查询为空
    if query:
        # 根据姓名筛选员工
        employees = Employee.objects.filter(name__icontains=query)
    else:
        # 如果没有查询条件，则获取所有员工
        employees = Employee.objects.all()
    
    return render(request, 'admin/admin_employee_list.html', {'employees': employees, 'query': query})


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
    
    return render(request, 'admin/admin_edit_employee.html', {'form': form, 'employee': employee})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def my_view(request):
    # 处理表单提交
    pass



@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user  # 关联当前用户
            leave_request.save()
            return redirect('user:leave_history')  # 重定向到查看请假记录
    else:
        form = LeaveRequestForm()

    return render(request, 'employee/apply_leave.html', {'form': form})


@login_required
def leave_history(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('start_date')
    return render(request, 'employee/leave_history.html', {'leave_requests': leave_requests})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def manage_leave_requests(request):
    leave_requests = LeaveRequest.objects.all().order_by('start_date')
    return render(request, 'admin/manage_leave_requests.html', {'leave_requests': leave_requests})


@staff_member_required
def review_leave_request(request, leave_id, action):
    leave_request = LeaveRequest.objects.get(id=leave_id)
    if action == 'approve':
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
    elif action == 'reject':
        leave_request.status = 'rejected'
        leave_request.approved_by = request.user
    leave_request.save()
    return redirect('user:manage_leave_requests')


from django.utils.timezone import now

@login_required
def employee_attendance(request):

    attendance, created = Attendance.objects.get_or_create(
        employee=request.user,
        created_at=now().date()
    )

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            # 获取表单数据
            check_in_time = form.cleaned_data.get('check_in_time')  # 签到时间
            check_out_time = form.cleaned_data.get('check_out_time')  # 签退时间

            # 确保时间是字符串格式，或转换为合适的格式
            if check_in_time:
                attendance.check_in_time = now().replace(
                    hour=check_in_time.hour, minute=check_in_time.minute, second=0
                )
            if check_out_time:
                attendance.check_out_time = now().replace(
                    hour=check_out_time.hour, minute=check_out_time.minute, second=0
                )

            form.save()

            # 自动判断考勤状态
            settings = AttendanceSettings.objects.first()
            if settings:
                if (attendance.check_in_time.time() > settings.start_time or
                        attendance.check_out_time.time() < settings.end_time):
                    attendance.status = 'abnormal'
                else:
                    attendance.status = 'normal'
            attendance.save()
            return redirect('user:attendance_history')
    else:
        form = AttendanceForm(instance=attendance)

    return render(request, 'employee/attendance.html', {'form': form, 'attendance': attendance})



@login_required
def attendance_history(request):
    """员工查看考勤记录"""
    records = Attendance.objects.filter(employee=request.user).order_by('-created_at')
    return render(request, 'employee/attendance_history.html', {'records': records})


@staff_member_required
def manage_attendance_settings(request):
    """管理员设置上下班时间"""
    settings = AttendanceSettings.objects.first()
    if request.method == 'POST':
        form = AttendanceSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('user:manage_attendance')
    else:
        form = AttendanceSettingsForm(instance=settings)

    return render(request, 'admin/attendance_settings.html', {'form': form})


@staff_member_required
def manage_attendance(request):
    """管理员查看考勤记录"""
    records = Attendance.objects.all().order_by('-created_at')
    attendance_stats = all_attendance_records(request)
    return render(request, 'admin/manage_attendance.html', {'records': records, 'attendance_stats': attendance_stats})


from django.db.models import Count, Q

def all_attendance_records(request):
    
    # 按照员工分组，统计正常和异常的次数
    attendance_stats = Attendance.objects.values('employee__username').annotate(
        normal_count=Count('status', filter=Q(status='normal')),
        abnormal_count=Count('status', filter=Q(status='abnormal'))
    )

    return attendance_stats
