from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import (
    AppUser,
    MembershipPlan,
    Customer,
    Equipment,
    Payment,
    Expense,
)
from .serializers import (
    AppUserSerializer,
    MembershipPlanSerializer,
    CustomerSerializer,
    EquipmentSerializer,
    PaymentSerializer,
    ExpenseSerializer,
)


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [AllowAny]


class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [AllowAny]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-enrolled_on')
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-paid_on')
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-expense_date')
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
