from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


class AppUser(models.Model):
    """Simplified user model (separate from django.contrib.auth.User)."""
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:
        return self.username


class MembershipPlan(models.Model):
    id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=200, default='Standard Plan')
    # Default to a common monthly plan (30 days) and price 0.00 if not provided
    validity_days = models.PositiveIntegerField(help_text='Validity in days', default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self) -> str:
        return f"{self.plan_name} ({self.validity_days}d)"


class Customer(models.Model):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('O', 'Other'))

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    enrolled_on = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=100, default='Pending')
    medical_notes = models.TextField(blank=True)
    attendance_history = models.TextField(blank=True)
    time_slot = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        # Auto-calc expiry if plan present and expiry not set
        if self.plan and not self.expiry_date:
            self.enrolled_on = self.enrolled_on or timezone.now().date()
            self.expiry_date = self.enrolled_on + timedelta(days=int(self.plan.validity_days))
        super().save(*args, **kwargs)


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=100, default='Active')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.name


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=100, default='Cash')
    paid_on = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Payment {self.id} - {self.customer.name} - {self.amount}"


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.category} - {self.amount}"

