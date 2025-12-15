from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bestsellers
from .serializers import BestsellerSerializer


@api_view(["GET"])
def bestseller_list(request):
    serializer = BestsellerSerializer(Bestsellers.objects.all(), many=True)
    return Response(serializer.data)
