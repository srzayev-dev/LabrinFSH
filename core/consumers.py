import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import Post, Comment


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            "type" : "websocket.accept"
        })
        # await asyncio.sleep(10)
        file_id = self.scope['url_route']['kwargs']['file_id']
        me = self.scope['user']

        print(file_id, me)
        await self.send({
            "type" : "websocket.send",
            "text" : "Hello World"
        })
        

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def websocket_receive(self, event):
        print('receive', event)
