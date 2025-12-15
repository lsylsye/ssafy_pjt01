from rest_framework import serializers
from .models import Bestsellers

class BestsellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bestsellers
        fields = [
            "id",
            "category",
            "category_name",
            "title",
            "author",
            "publisher",
            "cover",
            "best_rank",
            "sales_point",
            "customer_review_rank",
        ]
