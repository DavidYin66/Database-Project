# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Employee

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
