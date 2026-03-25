from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "full_name", "bio", "location", "skills"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        skill_names = validated_data.pop("skills", [])
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name.strip().lower())
            user.skills.add(skill)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been deactivated.")
        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "full_name", "bio", "location", "skills", "date_joined"]
