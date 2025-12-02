from django.contrib import admin
from .models import MembershipPlan, Customer, Equipment, Payment, Expense, AppUser


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'validity_days', 'price')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_number', 'email', 'plan', 'enrolled_on', 'expiry_date')
    search_fields = ('name', 'mobile_number', 'email')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'plan', 'amount', 'method', 'paid_on')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'expense_date')


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email')
