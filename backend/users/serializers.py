from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()     

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)

    favorite_country = serializers.ChoiceField(
        choices=User.FAVORITE_COUNTRIES,
        required=False
    )
    favorite_genre = serializers.ChoiceField(
        choices=User.FAVORITE_GENRES,
        required=False
    )

    other_country = serializers.CharField(
        required=False,
        allow_blank=True
    )

    # ============================
    # 1) nickname 중복 검사
    # ============================
    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    # ============================
    # 2) email 중복 검사
    # ============================
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    # ============================
    # 3) 기타 선택 시 other_country
    # ============================
    def validate(self, attrs):
        favorite_country = attrs.get("favorite_country")
        other_country = attrs.get("other_country", "")

        # 기타 선택 -> 값 미입력 시 오류
        if favorite_country == "OTHER" and not other_country:
            raise serializers.ValidationError({
                "other_country": "기타 선택 시 국가를 직접 입력해야 합니다."
            })

        return attrs

    # ============================
    # 4) cleaned_data 정리
    # ============================
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["nickname"] = self.validated_data.get("nickname")
        data["favorite_country"] = self.validated_data.get("favorite_country")
        data["favorite_genre"] = self.validated_data.get("favorite_genre")
        data["other_country"] = self.validated_data.get("other_country")
        return data

    # ============================
    # 5) 저장 로직
    # ============================
    def save(self, request):
        user = super().save(request)

        user.nickname = self.validated_data.get("nickname")
        user.favorite_country = self.validated_data.get("favorite_country")
        user.favorite_genre = self.validated_data.get("favorite_genre")
        user.other_country = self.validated_data.get("other_country")

        user.save()
        return user
    
    
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "profile_image"]


