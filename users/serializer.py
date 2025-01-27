from shared.serializers import BaseSerializer

class TokenSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'key': instance.key,
            'created_at': instance.created_at.isoformat(),
        }
