from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import GameCreationSerializer, PurchaseSerializer
from .services import *


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

            game_creator = find_game_creator(game_id)
            game_price = find_game_price(game_id)
            username = self.request.user.username
            user_balance = self.request.user.balance
            user = find_user(username)

            if user_balance >= game_price:
                game_purchase(user, game_price, game_creator)
                self.perform_create(serializer)
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
