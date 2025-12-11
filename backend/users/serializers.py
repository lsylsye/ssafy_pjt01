from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False)
    favorite_country = serializers.CharField(required=False)
    other_country = serializers.CharField(required=False)
    favorite_genre = serializers.CharField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname')
        data['favorite_country'] = self.validated_data.get('favorite_country')
        data['other_country'] = self.validated_data.get('other_country')
        data['favorite_genre'] = self.validated_data.get('favorite_genre')
        return data

    def save(self, request):
        user = super().save(request)

        user.nickname = self.cleaned_data.get('nickname')
        user.favorite_country = self.cleaned_data.get('favorite_country')
        user.other_country = self.cleaned_data.get('other_country')
        user.favorite_genre = self.cleaned_data.get('favorite_genre')

        user.save()
        return user
