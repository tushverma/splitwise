from rest_framework import serializers
from splitwise import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def create(self, validated_data):
        """Creates and returns a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Debt
        fields = ('id', 'from_user', 'to_user', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'group_name', 'debts', 'members')


class ExpenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpenseUser
        fields = ('id', 'paid_share', 'owed_share', 'net_balance')


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = ('group_id', 'description', 'payment',
                  'date', 'friendship_id', 'repayments',
                  'user', 'transaction_id')
