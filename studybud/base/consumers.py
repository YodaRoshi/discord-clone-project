import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, Room, User
from .helpers import timesince


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name'].replace(' ','_')
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)
        body = data['body']
        username = data['username']
        room_name = data['room']

        message = await self.save_message(username, room_name, body)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': message,
            }
        )   

    
    async def send_message(self,event):
        obj = event['message']
        created = timesince(obj.created)

        json_str = json.dumps({
            'message_id' : obj.id,
            'user_id': obj.user.id,
            'username': obj.user.username,
            'body': obj.body,
            'avatar': obj.user.avatar.url,
            'created' : created,
            'is_superuser' : obj.user.is_superuser,
            'is_active' : True
        },indent=4)

        await self.send(text_data=json_str)

    @sync_to_async
    def save_message(self,username, room_name,body):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room_name)
        message = Message.objects.create(
            user=user,
            room=room,
            body=body
        )
        room.participants.add(user)
        return message
