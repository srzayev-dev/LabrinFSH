import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import Post, Comment
User = get_user_model()

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            "type" : "websocket.accept"
        })
        # await asyncio.sleep(10)
        file_id = self.scope['url_route']['kwargs']['file_id']
        self.room = str(file_id)
        print('here', self.room)
        await self.channel_layer.group_add(
            self.room,
            self.channel_name,
        )
        

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def websocket_receive(self, event):
        new_comment_data = event.get('text')
        new_comment = json.loads(new_comment_data)
        user = self.scope['user']
        comment_text = new_comment['comment_text']
        file_id = self.scope['url_route']['kwargs']['file_id']
        message = await self.create_comment(user, comment_text, file_id)
        comment = {
            'comment_text': comment_text,
            'username': user.username,
        }
        await self.channel_layer.group_send(
            self.room,
            {
                'type': 'show_comment',
                'text': json.dumps(comment),
            }
        )

    @database_sync_to_async
    def get_file_id(self, file_id):
        return str(Post.objects.get(id=int(file_id)).id)

    @database_sync_to_async
    def create_comment(self, author, comment_text, file_field_id):
        file = Post.objects.get(id=file_field_id)
        message = Comment(
            user=author,
            content=comment_text,
            file=file,
        )
        message.save()
        return message

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })