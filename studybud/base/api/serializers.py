# python objects can not be converted automatically into json unlike dictionaries.
# serializers are classes that take a certain model that we want to serialize and turn it into a json object.

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'