from rest_framework import serializers
from .models import CustomUser, Deposit
from games.serializers import PurchaseProfileSerializer
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=5)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'password'
        ]

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError({"Message": "duplicate",
                                               "Description": "Not successful, such user already exists"})

        errors = dict()
        try:
            validators.validate_password(password=password)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = [
            "id",
            "amount",
        ]


class DepositsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = ['id',
                  'amount']


class RollbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = ['id',
                  'amount']


class ProfileSerializer(serializers.ModelSerializer):
    games = serializers.SerializerMethodField()

    def get_games(self, instance):
        purchases = instance.purchases.all()
        return PurchaseProfileSerializer(purchases, many=True).data

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'balance',
            'games',
            'created_games'
        ]
