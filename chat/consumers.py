import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        
        # Print debug information
        print(f"Connecting to room: {self.room_group_name}")
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"Successfully connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        print(f"Disconnecting from {self.room_group_name}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            sender_id = data['sender']
            receiver_id = data['receiver']

            # Save the message
            await self.save_message(sender_id, receiver_id, message)

            # Send to the group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': sender_id,
                    'receiver': receiver_id,
                    'timestamp': timezone.now().strftime("%H:%M")
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                'message': event['message'],
                'sender': event['sender'],
                'receiver': event['receiver'],
                'timestamp': event['timestamp']
            }))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            return Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content
            )
        except Exception as e:
            print(f"Error saving message: {str(e)}")
            raise