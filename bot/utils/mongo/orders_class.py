

import logging

from pymongo.errors import DuplicateKeyError

from .setup_db import collection_orders


class Orders:
    '''Распоряжения'''
    async def add_order(order: dict) -> bool:
        event_to_add = {
            'year': order.get('year'),
            'month': order.get('month'),
            'link': order.get('link')
        }
        try:
            collection_orders.insert_one(event_to_add)
            return True
        except DuplicateKeyError as d:
            logging.error(d)
            return False

    async def delete_order(year: int, month: int) -> bool:
        """Удаляем распоряжение"""
        try:
            zap = collection_orders.find_one_and_delete({'year': year, 'month': month})
            if zap:
                return True
            return False
        except Exception as e:
            logging.error(e)
            return False

    async def get_all_orders() -> list | bool:
        """Получаем все распоряжения"""
        try:
            return list(collection_orders.find({}))
        except Exception as e:
            logging.error(e)
            return False
