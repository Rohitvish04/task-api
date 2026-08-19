from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "manager"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role", "manager"]

    def validate(self, data):
        role = data.get("role", "USER")
        manager = data.get("manager")

        # keeping this check here instead of the model - it's a business
        # rule (only Users have a manager), not a database constraint
        if role == "USER" and not manager:
            raise serializers.ValidationError("manager is required when role is USER")
        if role != "USER" and manager:
            raise serializers.ValidationError("only role USER can have a manager assigned")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
