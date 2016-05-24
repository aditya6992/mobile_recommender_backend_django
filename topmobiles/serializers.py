from rest_framework import serializers
from models import Mobile

class mobileSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    camera = serializers.FloatField(required=False)
    ram = serializers.IntegerField(required=False)
    storage = serializers.IntegerField(required=False)
    battery = serializers.IntegerField(required=False)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.url = attrs.get('url', instance.url)
            instance.name = attrs.get('name', instance.name)
            instance.camera = attrs.get('camera', instance.camera)
            instance.ram = attrs.get('ram', instance.ram)
            instance.storage = attrs.get('storage', instance.storage)
            instance.battery = attrs.get('battery', instance.battery)
            return instance

        return Mobile(attrs.get('url'), attrs.get('name'), attrs.get('camera'), attrs.get('ram'), attrs.get('storage'),
                      attrs.get('battery'))