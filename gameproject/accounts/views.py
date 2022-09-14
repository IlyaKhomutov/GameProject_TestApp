from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from .models import Deposit, CustomUser
from .serializers import RegistrationSerializer, DepositSerializer, DepositsListSerializer, RollbackSerializer, \
    ProfileSerializer
from django.db.models import F


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(not (request.user and request.user.is_authenticated))


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "success", "Description": "Success"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"Message": "error", "Description": "Not successful, unknown error"},
                            status=status.HTTP_400_BAD_REQUEST)


class DepositViewSet(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        amount = (request.data['amount'])
        username = self.request.user.username
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            user = CustomUser.objects.filter(username=username)
            user.update(balance=F('balance') + amount)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"deposit_id": serializer.data['id'], "balance": int(self.request.user.balance) + int(amount),
                 "Message": "success", "Description": "Success"},
                status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({"Message": "error", "Description": "Not successful, unknown error"},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DepositsListViewSet(viewsets.ModelViewSet):
    serializer_class = DepositsListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        my_id = self.request.user.id
        queryset = Deposit.objects.filter(user_id=my_id)
        return queryset


class RollbackView(generics.RetrieveUpdateAPIView):
    queryset = Deposit.objects.all()
    serializer_class = RollbackSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        deposit_amount = instance.amount
        deposit_id = instance.id
        deposit_status = instance.status
        deposit = Deposit.objects.filter(id=deposit_id)

        username = self.request.user.username
        user = CustomUser.objects.filter(username=username)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if serializer.is_valid(raise_exception=True):
            if deposit_status == "success":
                if self.request.user.balance >= deposit_amount:
                    self.perform_update(serializer)
                    deposit.update(status='cancelled')
                    user.update(balance=F('balance') - deposit_amount)
                    return Response(
                        {"balance": int(self.request.user.balance) - int(deposit_amount),
                         "Message": "success", "Description": "Success"},
                        status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"Message": "error",
                         "Description": "Not successful, there are not enough money in your account"},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"Message": "error", "Description": "Not successful, deposit is already cancelled"},
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"Message": "error", "Description": "Not successful, unknown error"},
                status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_object(self):
        return self.request.user
