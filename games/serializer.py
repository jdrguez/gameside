from shared.serializers import BaseSerializer
from categories.serializer import CategorySerializer
from platforms.serializer import PlatformSerializer

class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description, 
            'cover':self.build_url(instance.cover.url),
            'price': float(instance.price),
            'released_at': instance.released_at.isoformat(),
            'pegi': instance.get_pegi_display(),
            'stock': instance.stock,
            'category': CategorySerializer(instance.category).serialize(),
            'platforms': PlatformSerializer(instance.platforms.all(), request=self.request).serialize()

        }
