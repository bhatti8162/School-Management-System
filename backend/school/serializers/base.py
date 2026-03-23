from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = self._replace_empty_with_na(data)
        return data

    def _replace_empty_with_na(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None or value == '':
                    data[key] = 'N/A'
                elif isinstance(value, dict):
                    data[key] = self._replace_empty_with_na(value)
                elif isinstance(value, list):
                    data[key] = [self._replace_empty_with_na(item) if isinstance(item, dict) else item for item in value]
        return data