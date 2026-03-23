from .base import *

class UniversalSearchViewSet(viewsets.ViewSet):

    def get_model_by_name(self, model_name):
        for app_config in apps.get_app_configs():
            for name, model in app_config.models.items():
                if name.lower() == model_name.lower():
                    return model
        return None

    @action(detail=False, methods=['get'], url_path=r'(?P<model_name>\w+)')
    def search(self, request, model_name=None):
        keyword = request.query_params.get("q")

        if not keyword:
            return Response({"error": "Use ?q="}, status=400)

        model = self.get_model_by_name(model_name)
        if not model:
            return Response({"error": "Model not found"}, status=400)

        text_fields = [
            f.name for f in model._meta.get_fields()
            if f.get_internal_type() in ('CharField', 'TextField')
        ]

        query = Q()
        for field in text_fields:
            query |= Q(**{f"{field}__icontains": keyword})

        results = model.objects.filter(query)

        serializer_class = type(
            "DynamicSerializer",
            (serializers.ModelSerializer,),
            {
                "Meta": type("Meta", (), {
                    "model": model,
                    "fields": [f.name for f in model._meta.fields]
                })
            }
        )

        return Response(serializer_class(results, many=True).data)