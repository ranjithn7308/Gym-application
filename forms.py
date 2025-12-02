from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, MembershipPlan, Equipment, Payment, AppUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Admin ID'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'mobile_number', 'email', 'gender', 'date_of_birth',
            'address', 'height', 'weight', 'plan', 'time_slot'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = Customer.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('Email already registered for another customer.')
        return email


class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['plan_name', 'validity_days', 'price']


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'status', 'quantity']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['customer', 'plan', 'amount', 'method', 'notes']


class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ['username', 'password', 'name', 'contact_number', 'email']
        