from rest_framework import serializers


class GrassLegendSerializer(serializers.Serializer):
    legend = serializers.ListField(child=serializers.CharField())
    cap = serializers.IntegerField()


class GrassDaySerializer(serializers.Serializer):
    date = serializers.CharField()
    points = serializers.IntegerField()
    points_capped = serializers.IntegerField()
    bucket = serializers.CharField()


class GrassResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    days = serializers.IntegerField()
    legend = GrassLegendSerializer()
    items = GrassDaySerializer(many=True)


class LevelSerializer(serializers.Serializer):
    exp_total = serializers.IntegerField()
    level = serializers.IntegerField()
    next_level_start_exp = serializers.IntegerField()
