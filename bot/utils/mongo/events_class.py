

import logging
import time

from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

from .setup_db import collection_events


class Events:
    event_status = {
        "valid": 0,
        "invalid": 1
    }

    def __init__(self):
        pass

    async def add_event(self, event: dict) -> bool:
        event_to_add = {
            'author': event.get('author'),
            # 'title': event.get('title'),
            # 'media': event.get('media'),
            # 'media_type': event.get('media_type'),
            'text': event.get('text'),
            'jazz': event.get('jazz'),
            # 'places': int(event.get('places')),  # Всего мест
            # 'participants': [],  # Участники
            'timestamp': event.get('timestamp'),
            # 'order_path': event.get('order_path'),
            # 'status': self.event_status["valid"],  # valid, not valid
            'notified': False,  # valid 1, not valid 0
        }
        try:
            collection_events.insert_one(event_to_add)
            return True
        except DuplicateKeyError as d:
            logging.error(d)
            logging.error(f'Duplicate Error: {event}')
            return False

    async def delete(_id: str) -> bool:
        """Удаление мероприятия"""
        try:
            collection_events.delete_one({'_id': ObjectId(_id)})
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def hide_or_show(_id: str, type: bool) -> bool:
        """Скрываем(от голосования) мероприятие"""
        try:
            collection_events.update_one({'_id': ObjectId(_id)}, {"$set": {'status': type}})
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def set_notified(_id: str, status: int) -> bool:
        """Устанавливаем тип прошедшего уведомления"""
        try:
            collection_events.update_one({'_id': ObjectId(_id)}, {"$set": {'notified': status}})
            return True
        except Exception as e:
            logging.error(e)
            return False
#######################

    async def get_all_future_events(is_admin: bool = False) -> list | bool:
        """выдаёт будущие мероприятия
        (> =) больше чем равно - $ gte
        """
        command = {
            'timestamp': {'$gte': int(time.time())}
        }
        if not is_admin:
            command['status'] = 1
        try:
            return list(collection_events.find(command))
        except Exception as e:
            logging.error(e)
            return False

    async def get_events_for_next_day(is_admin: bool = False) -> list | bool:
        """выдаёт будущие мероприятия на предстоящий день
        (> =) больше чем равно - $ gte
        """
        now = int(time.time())
        command = {
            'timestamp': {
                '$gte': now,
                '$lte': now+86400  # + День
            }
        }
        if not is_admin:
            command['status'] = 1
        try:
            return list(collection_events.find(command))
        except Exception as e:
            logging.error(e)
            return False
#######################

    async def get_all() -> list | bool:
        """Получаем все мероприятия"""
        command = {}
        # if not is_admin:
        #     command['status'] = 1
        try:
            return list(collection_events.find(command).sort('timestamp', -1))
        except Exception as e:
            logging.error(e)
            return False

    async def get_one(_id: str) -> dict | bool:
        """Получаем мероприятие по id"""
        try:
            return collection_events.find_one({'_id': ObjectId(_id)})
        except Exception as e:
            logging.error(e)
            return False

    async def get_all_my(user_id: int, is_admin: bool = False) -> list | bool:
        """Все мероприятия в которых я участвую"""
        command = {
            'participants': {"$in": [user_id]}
        }
        if not is_admin:
            command['status'] = 1
        try:
            return list(collection_events.find(command).sort('timestamp', -1))
        except Exception as e:
            logging.error(e)
            return False

#######################

    async def add_participant(user_id: int, event_id: str) -> list | bool:
        """Добавление участника"""
        try:
            return list(collection_events.find_one_and_update(
                {'_id': ObjectId(event_id)},
                {
                    '$addToSet': {
                        'participants': user_id
                    }
                },
                upsert=False
            )
            )
        except Exception as e:
            logging.error(e)
            return False

    async def delete_participant(user_id: int, event_id: str) -> list | bool:
        """Удаление участника"""
        try:
            return list(collection_events.find_one_and_update(
                {'_id': ObjectId(event_id)},
                {
                    '$pull': {
                        'participants': user_id
                    }
                },
                upsert=False
            )
            )
        except Exception as e:
            logging.error(e)
            return False

    async def delete_order_path(_id: str) -> bool:
        """Удаляем путь к распоряжению"""
        try:
            collection_events.update_one({'_id': ObjectId(_id)}, {"$set": {'order_path': None}})
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def add_order_path(_id: str, path: str) -> bool:
        """Добавляем путь к распоряжению"""
        try:
            collection_events.update_one({'_id': ObjectId(_id)}, {"$set": {'order_path': path}})
            return True
        except Exception as e:
            logging.error(e)
            return False

    async def get_all_orders(is_admin: bool = False) -> list | bool:
        """Добавляем путь к распоряжению"""
        command = {'order_path': {
            # '$not': {'$size':  0},
            '$ne': None,
            '$exists': True
        }}

        if not is_admin:
            command['status'] = 1
        try:
            return list(collection_events.find(command, {'order_path': 1, 'title': 1, 'timestamp': 1}))
        except Exception as e:
            logging.error(e)
            return False

    async def get_all_in_interval(start: int, end: int) -> list | bool:
        """Добавляем путь к распоряжению"""
        try:
            return list(collection_events.find({
                'timestamp': {
                        '$gte': start,
                        '$lt': end},
                'order_path': {
                    '$ne': None,
                    '$exists': True
                }
            }, {
                'order_path': 1, 'title': 1, 'timestamp': 1
            }
            ))
        except Exception as e:
            logging.error(e)
            return False
