import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer

# from .models import Like


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add('like_updates', self.channel_name) #"online"

        await self.accept()

    async def disconnect(self, close_code):

        pass

    async def handle_like(self, message):
        # like = event['like']
        print(message)

        # Send message to WebSocket
        await self.send(json.dumps({
            'author_id': [message['message']['author_id']],
            'message': f"{message['message']['user']} понравилась ваша статья: {message['message']['arcticle']}",
        }))


    async def user_commented(self, message):
        """
        Simple echo handler for telegram messages in any chat.
        """
        await self.send(json.dumps({
            "type": "telegram.message",
            "text": "You said: %s" % message["message"],
        }))


# @receiver(post_save, sender=Like)
# async def handle_new_like(sender, instance, **kwargs):
#     # Get the Like data
#     like_data = await get_like_data(instance)

#     # Send message through WebSocket
#     channel_layer = get_channel_layer()
#     # await channel_layer.group_send(
#     #     'like_updates',
#     #     {
#     #         'type': 'handle_like',
#     #         'like': like_data,
#     #     }
#     # )
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         'like_updates',
#         {
#             'type': 'handle_like',
#             'message': like_data
#         }
#     )
