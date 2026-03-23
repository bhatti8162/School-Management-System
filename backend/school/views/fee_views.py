from .base import *

from ..models.fee import Fee
from ..serializers import FeeSerializer


class FeeViewSet(ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer