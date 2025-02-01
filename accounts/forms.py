from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# 作成したユーザーのモデルデータを返す
User = get_user_model()

# ユーザー情報を作成するクラス
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Password再入力",widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username', 'email','password']
    # パスワードのチェック
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError("パスワードが一致しません")
    # セーブのカスタマイズ
    def save(self,commit=False):
        user =super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user

# ユーザー情報を変更するクラス
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    website = forms.URLField(required=False)
    picture = forms.FileField(required=False)

    class Meta:
        fields= ("username","email","password","is_staff","is_active","is_superuser","website","picture")

    def clean_password(self):
        # すでに登録されているパスワードを返す
        return self.initial["password"]