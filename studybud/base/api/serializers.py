# python objects can not be converted automatically into json unlike dictionaries.
# serializers are classes that take a certain model that we want to serialize and turn it into a json object.

from rest_framework.serializers import ModelSerializer
from .models import Room, Message, User, Topic


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TopicSerialzer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class RoomSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    topic = TopicSerialzer(many=False, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    room = RoomSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
