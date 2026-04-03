from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import FinanceRecordViewSet, UserRegisterView, summary_view

router = DefaultRouter()
router.register(r'records', FinanceRecordViewSet, basename='records')

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('records/summary/', summary_view, name='summary'),
    path('', include(router.urls)),
]
