from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random

from .models import Customer, MembershipPlan, Equipment, Payment
from .forms import LoginForm, CustomerForm, MembershipPlanForm, EquipmentForm, PaymentForm
from django.db import models
from django.db.utils import OperationalError


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm(request)
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def send_otp_simulation(request, user_identifier):
    otp = random.randint(100000, 999999)
    request.session['password_reset_otp'] = str(otp)
    request.session['password_reset_user'] = user_identifier
    messages.info(request, f'OTP (development): {otp}')


def request_password_reset(request):
    """Step 1: Admin supplies username/email; we generate OTP."""
    if request.method == 'POST':
        user_identifier = request.POST.get('identifier')
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=user_identifier)
        except User.DoesNotExist:
            messages.error(request, 'No such admin user')
            return redirect('request_password_reset')
        send_otp_simulation(request, user_identifier)
        return redirect('verify_otp')
    return render(request, 'request_password_reset.html')


def verify_otp(request):
    """Step 2: verify OTP and allow password reset."""
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp and request.session.get('password_reset_otp') == otp:
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')


def reset_password(request):
    """Step 3: set new password for the admin user (development flow)."""
    if not request.session.get('otp_verified'):
        return redirect('request_password_reset')
    if request.method == 'POST':
        pwd = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        if pwd != pwd2:
            messages.error(request, 'Passwords do not match')
        else:
            from django.contrib.auth.models import User
            username = request.session.get('password_reset_user')
            user = User.objects.get(username=username)
            user.set_password(pwd)
            user.save()
            # cleanup
            for k in ['password_reset_otp', 'password_reset_user', 'otp_verified']:
                if k in request.session:
                    del request.session[k]
            messages.success(request, 'Password updated. Please login.')
            return redirect('login')
    return render(request, 'reset_password.html')


@login_required
def dashboard(request):
    # Attempt to read DB-backed objects. During initial setup migrations may not
    # have been applied yet; guard against OperationalError so the page doesn't
    # crash and still renders a helpful message.
    try:
        plans = MembershipPlan.objects.all()
    except OperationalError:
        plans = []
    try:
        members = Customer.objects.all().order_by('-enrolled_on')[:5]
    except OperationalError:
        members = []

    attendance_pct = 85  # placeholder: implement attendance logic later
    # Simple revenue/expense placeholders (guard against missing tables during initial dev)
    try:
        revenue = Payment.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
    except OperationalError:
        revenue = 0
    context = {
        'plans': plans,
        'members': members,
        'attendance_pct': attendance_pct,
        'revenue': revenue,
    }
    return render(request, 'dashboard.html', context)


@login_required
def register_member(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # auto-calc expiry based on plan validity_days handled in model.save
            customer.save()
            messages.success(request, 'Customer registered')
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'register_member.html', {'form': form})


@login_required
def membership_plan_create(request):
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan added')
            return redirect('dashboard')
    else:
        form = MembershipPlanForm()
    return render(request, 'membership_plan_form.html', {'form': form})


@login_required
def list_members(request):
    qs = Customer.objects.all()
    return render(request, 'list_members.html', {'members': qs})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})
