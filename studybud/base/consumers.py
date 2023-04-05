import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Message, Room, User
from .serializers import MessageSerializer
from django.utils.timezone import localdate

import pytz
from datetime import datetime, timezone

utc=pytz.UTC

from dateutil.relativedelta import relativedelta
from django.utils.timesince import TIME_STRINGS as timesince_time_strings
from django.utils.html import avoid_wrapping
from django.utils.translation import gettext, get_language
import inflect 
p = inflect.engine()


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
        time_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        created = await self.timesince(time_now,obj.created)
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
    
    
    @sync_to_async
    def async_message_serializer(self,obj):
        return MessageSerializer(obj,many=False).data
    

    @sync_to_async
    def timesince(self,d, now):
        # test = datetime(2026, 6, 30, 8, 3, 2, 345784, tzinfo=timezone.utc)
        # test2 = datetime(2023, 7, 1, 10, 2, 1, 345784, tzinfo=timezone.utc)
        # delta = relativedelta(test, test2)

        delta = relativedelta(now, d)
        years = delta.years
        months = delta.months
        weeks = delta.days // 7
        days = delta.days - weeks * 7
        hours = delta.hours
        minutes = delta.minutes

        if (years > 0):
            return str(years) + " " + p.plural("year", years)
        elif (months > 0):
            return str(months) + " " + p.plural("month", months)
        elif (weeks > 0):
            return str(weeks) + " " + p.plural("week", weeks)
        elif (days > 0):
            return str(days) + " " + p.plural("day", days)
        elif (hours > 0):
            return str(hours) + " " + p.plural("hour", days)
        else:
            return str(minutes)+ " " + p.plural("minute", days)