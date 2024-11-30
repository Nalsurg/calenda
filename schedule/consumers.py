from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.apps import apps
from datetime import datetime
from django.utils.dateparse import parse_datetime
import logging
import json

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'event_group'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        event_data = json.loads(text_data)

        # Сохранение события в базе данных
        event = await self.save_event(event_data)

        # Подготовка данных для трансляции
        response_data = {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat() if isinstance(event.start, datetime) else event.start,
            'end': event.end.isoformat() if event.end and isinstance(event.end, datetime) else event.end,
            'resourceId': event.resourceId,
            'description': event.description,
        }

        # Трансляция данных события в группу
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'event_message',
                'event': response_data,
            }
        )

    async def event_message(self, event):
        await self.send(text_data=json.dumps(event['event']))

    @sync_to_async
    def save_event(self, data):
        # Ленивый доступ к модели Event
        Event = apps.get_model('schedule', 'Event')

        # Логирование входящих данных
        logger = logging.getLogger(__name__)
        logger.debug(f"Saving event with data: {data}")

        try:
            # Преобразование ISO 8601 строк в объекты datetime
            start = parse_datetime(data['start'])
            if not start:
                raise ValueError("Invalid start datetime format")
            end = parse_datetime(data.get('end')) if data.get('end') else None

            # Сохранение события в базе данных
            event = Event.objects.create(
                title=data['title'],
                start=start,
                end=end,
                description=data.get('description', ''),
                resourceId=data['resourceId']
            )

            # Лог успешного сохранения
            logger.info(f"Event saved successfully: {event}")
            return event

        except Exception as e:
            # Логирование ошибок
            logger.error(f"Error saving event: {e}")
            raise e