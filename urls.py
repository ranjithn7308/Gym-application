from django.urls import path, include
from . import api_views
from . import web_views as views
# import API function-based views from the API module
from . import views as api_functions

# API routes (Django REST Framework only)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', api_views.AppUserViewSet)
router.register(r'plans', api_views.MembershipPlanViewSet)
router.register(r'customers', api_views.CustomerViewSet)
router.register(r'equipment', api_views.EquipmentViewSet)
router.register(r'payments', api_views.PaymentViewSet)
router.register(r'expenses', api_views.ExpenseViewSet)

urlpatterns = [
    # auth / session endpoints
    path('api/auth/login/', api_functions.login_api, name='api_login'),
    path('api/auth/logout/', api_functions.logout_api, name='api_logout'),
    # password reset/OTP
    path('api/auth/password-reset/', api_functions.request_password_reset_api, name='api_password_reset'),
    path('api/auth/verify-otp/', api_functions.verify_otp_api, name='api_verify_otp'),
    path('api/auth/reset-password/', api_functions.reset_password_api, name='api_reset_password'),
    # dashboard and simple actions
    path('api/dashboard/', api_functions.dashboard_api, name='api_dashboard'),
    path('api/register-member/', api_functions.register_member_api, name='api_register_member'),
    path('api/plans/add/', api_functions.membership_plan_create_api, name='api_add_plan'),
    path('api/members/', api_functions.list_members_api, name='api_list_members'),
    path('api/members/<int:customer_id>/', api_functions.customer_detail_api, name='api_customer_detail'),

    # DRF router for CRUD on models
    path('api/', include((router.urls, 'gymapp'), namespace='api')),

    # optional: browsable API login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
