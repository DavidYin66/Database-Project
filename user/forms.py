# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Employee, LeaveRequest, Attendance, AttendanceSettings

def is_admin(user):
    return user.role == 'admin'

class UserProfileCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('admin', '管理员'), ('employee', '员工')], required=True)

    class Meta:
        model = UserProfile  # 使用自定义的 UserProfile 模型
        fields = ['username', 'password1', 'password2', 'role']  # 包括自定义字段 role



class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['id', 'name', 'gender', 'age', 'contact', 'salary', 'position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义字段顺序
        self.order_fields(['id', 'name', 'gender', 'age', 'contact', 'salary', 'position'])
        self.user = kwargs.get('instance', None)        # 获取当前用户
        if not is_admin(self.user.user):                 # 如果当前用户不是管理员
            self.fields['id'].disabled = True  # 禁止编辑 ID
        else:
            self.fields['id'].disabled = False


    def save(self, commit=True):
        # 处理保存逻辑：允许管理员修改 id
        instance = super().save(commit=False)
        
        if self.user and is_admin(self.user.user):
            # 如果当前用户是管理员，可以修改 ID
            instance.id = self.cleaned_data['id']

        if commit:
            instance.save()
        return instance


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),  # 使用 HTML5 日期选择器
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


# 员工考勤签到签退表单
class AttendanceForm(forms.ModelForm):
    check_in_time = forms.TimeField(
        label="签到时间",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False
    )
    check_out_time = forms.TimeField(
        label="签退时间",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False
    )

    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time']


# 管理员设置上下班时间表单
class AttendanceSettingsForm(forms.ModelForm):
    start_time = forms.TimeField(
        label="上班时间",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )
    end_time = forms.TimeField(
        label="下班时间",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=True
    )

    class Meta:
        model = AttendanceSettings
        fields = ['start_time', 'end_time']