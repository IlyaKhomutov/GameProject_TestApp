from django.db.models import F
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Game, Purchase
from .serializers import GameCreationSerializer, PurchaseSerializer
from accounts.models import CustomUser


class GameCreationViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameCreationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"game_id": serializer.data['id'], "Message": "success", "Description": "Success"},
                            status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({"Message": "error", "Description": "Not successful, unknown error"},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class GamePurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            game_id = request.data['game']

            game_creator = Game.objects.values_list('creator').get(id=game_id)[0]
            game_creator_user = CustomUser.objects.filter(id=game_creator)

            game_price = Game.objects.values_list('price').get(id=game_id)
            game_price = game_price[0]

            username = self.request.user.username
            user_balance = self.request.user.balance
            user_q = CustomUser.objects.filter(username=username)

            if user_balance >= game_price:
                user_q.update(balance=F('balance') - game_price)
                self.perform_create(serializer)
                game_creator_user.update(balance=F('balance') + game_price)
                headers = self.get_success_headers(serializer.data)
                return Response({"game_id": game_id, "balance": int(self.request.user.balance) - game_price,
                                 "Message": "success", "Description": "Success"}, status=status.HTTP_200_OK,
                                headers=headers)
            else:
                return Response({"Message": "insufficient_funds", "Description": "Not successful, insufficient funds"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": "error", "Description": "Not successful, unknown error"},
                            status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
