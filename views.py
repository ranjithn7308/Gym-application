from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
import random

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Customer, MembershipPlan, Payment
from .serializers import CustomerSerializer, MembershipPlanSerializer
from django.db import models
from django.db.utils import OperationalError


@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'Logged in'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    logout(request)
    return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)


def _send_otp(request, user_identifier):
    otp = random.randint(100000, 999999)
    request.session['password_reset_otp'] = str(otp)
    request.session['password_reset_user'] = user_identifier
    return otp


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset_api(request):
    identifier = request.data.get('identifier')
    if not identifier:
        return Response({'detail': 'identifier is required'}, status=status.HTTP_400_BAD_REQUEST)
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        return Response({'detail': 'No such admin user'}, status=status.HTTP_404_NOT_FOUND)
    otp = _send_otp(request, identifier)
    # For development we return the OTP in the response. Remove in production.
    return Response({'detail': 'OTP generated', 'otp': otp}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_api(request):
    otp = request.data.get('otp')
    if otp and request.session.get('password_reset_otp') == str(otp):
        request.session['otp_verified'] = True
        return Response({'detail': 'OTP verified'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_api(request):
    if not request.session.get('otp_verified'):
        return Response({'detail': 'OTP not verified'}, status=status.HTTP_403_FORBIDDEN)
    pwd = request.data.get('password')
    pwd2 = request.data.get('password2')
    if pwd != pwd2:
        return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    from django.contrib.auth.models import User
    username = request.session.get('password_reset_user')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.set_password(pwd)
    user.save()
    for k in ['password_reset_otp', 'password_reset_user', 'otp_verified']:
        if k in request.session:
            del request.session[k]
    return Response({'detail': 'Password updated'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    try:
        plans = MembershipPlan.objects.all()
    except OperationalError:
        plans = []
    try:
        members = Customer.objects.all().order_by('-enrolled_on')[:5]
    except OperationalError:
        members = []
    attendance_pct = 85
    try:
        revenue = Payment.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
    except OperationalError:
        revenue = 0
    data = {
        'plans': [MembershipPlanSerializer(p).data for p in plans],
        'members': [CustomerSerializer(m).data for m in members],
        'attendance_pct': attendance_pct,
        'revenue': revenue,
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_member_api(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def membership_plan_create_api(request):
    serializer = MembershipPlanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_members_api(request):
    qs = Customer.objects.all()
    serializer = CustomerSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_detail_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)



