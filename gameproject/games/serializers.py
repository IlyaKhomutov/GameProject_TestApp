from rest_framework import serializers
from .models import Game, Purchase


class GameCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if Game.objects.filter(title=data['title']).exists():
            raise serializers.ValidationError("This game already exists!")
        return data

    def create(self, validated_data):
        return Game.objects.create(**validated_data)

    class Meta:
        model = Game
        fields = [
            'id',
            'title',
            'price', ]


class PurchaseProfileSerializer(serializers.ModelSerializer):
    game = serializers.CharField()

    class Meta:
        model = Purchase
        fields = ["game"]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["game"
                  ]

    def validate(self, data):
        request = self.context.get('request', None)
        user = request.user
        if Purchase.objects.filter(user=user, game=data['game']).exists():
            raise serializers.ValidationError("You have already purchased this game!")
        return data

    def create(self, validated_data):
        return Purchase.objects.create(**validated_data)
