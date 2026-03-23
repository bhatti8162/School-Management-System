from .base import *

from ..models.result import Result
from ..serializers import ResultSerializer


class ResultViewSet(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer