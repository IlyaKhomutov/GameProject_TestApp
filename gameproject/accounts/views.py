from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from .models import Deposit, CustomUser
from .serializers import RegistrationSerializer, DepositSerializer, DepositsListSerializer, RollbackSerializer,\
    ProfileSerializer
from django.db.models import F


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(not(request.user and request.user.is_authenticated))


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


class RollbackView(generics.RetrieveDestroyAPIView):
    queryset = Deposit.objects.all()
    serializer_class = RollbackSerializer
    lookup_field = 'id'
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        amount = instance.amount

        username = self.request.user.username
        user = CustomUser.objects.filter(username=username)

        if self.request.user.balance >= amount:
            self.perform_destroy(instance)
            user.update(balance=F('balance') - amount)
            return Response(
                {"balance": int(self.request.user.balance) - int(amount),
                 "Message": "success", "Description": "Success"},
                status=status.HTTP_200_OK)
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
