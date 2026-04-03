from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import FinanceRecord
from .permissions import IsAdminOrReadOnly, IsRecordOwnerOrAdmin
from .serializers import FinanceRecordSerializer, UserSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # Serializer handles password hashing via create() method
    # keep perform_create in place for explicit clarity
    def perform_create(self, serializer):
        serializer.save()


class FinanceRecordViewSet(viewsets.ModelViewSet):
    queryset = FinanceRecord.objects.all()
    serializer_class = FinanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecordOwnerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category', 'description', 'transaction_type']
    ordering_fields = ['date', 'amount', 'created_at']

    def get_queryset(self):
        user = self.request.user
        queryset = FinanceRecord.objects.all()
        if hasattr(user, 'profile') and user.profile.role != 'admin':
            queryset = queryset.filter(user=user)

        tran_type = self.request.query_params.get('transaction_type')
        category = self.request.query_params.get('category')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if tran_type in ['income', 'expense']:
            queryset = queryset.filter(transaction_type=tran_type)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def summary_view(request):
    user = request.user
    if hasattr(user, 'profile') and user.profile.role == 'admin':
        records = FinanceRecord.objects.all()
    else:
        records = FinanceRecord.objects.filter(user=user)

    total_income = records.filter(transaction_type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = records.filter(transaction_type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    category_data = records.values('category').annotate(
        income=Sum('amount', filter=models.Q(transaction_type='income')),
        expense=Sum('amount', filter=models.Q(transaction_type='expense')),
    )

    monthly = (
        records
        .annotate(month=models.functions.TruncMonth('date'))
        .values('month')
        .annotate(
            total_income=Sum('amount', filter=models.Q(transaction_type='income')),
            total_expense=Sum('amount', filter=models.Q(transaction_type='expense')),
        )
        .order_by('-month')[:12]
    )

    recent = FinanceRecordSerializer(records.order_by('-date', '-created_at')[:10], many=True).data

    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_breakdown': list(category_data),
        'monthly': list(monthly),
        'recent_activity': recent,
    })
