import time

from pymongo.errors import DuplicateKeyError

from .setup_db import collection_users


class User:
    """
    User class
    """

    def __init__(self, user_id):
        self.user_id = user_id

    async def get_info(self):
        return collection_users.find_one({'_id': self.user_id})

    async def get_all(self) -> list:
        '''Возвращает всех пользователей'''
        return list(collection_users.find({}))

    async def update_user(self, user: dict) -> bool:
        try:
            collection_users.update_one({
                '_id': self.user_id
            }, {"$set": {
                'last_name': user.get('full_name')[0],  # Фамилия
                'first_name': user.get('full_name')[1],  # Имя
                'patronymic': user.get('full_name')[2],  # Отчество
                'email': user.get('email'),
                'university': user.get('university'),
                'faculty': user.get('faculty'),
                'course': user.get('course'),
                'phone_number': user.get('phone_number'),
                # 'is_admin': False,
            }})
            return True
        except Exception:
            return False

    async def register_user(self, user: dict) -> bool:
        user_to_add = {
            '_id': self.user_id,
            'last_name': user.get('full_name')[0],  # Фамилия
            'first_name': user.get('full_name')[1],  # Имя
            'patronymic': user.get('full_name')[2],  # Отчество
            'email': user.get('email'),
            'university': user.get('university'),
            'faculty': user.get('faculty'),
            'course': user.get('course'),
            'phone_number': user.get('phone_number'),
            # 'phone_number': phone_number,
            'is_admin': False,
            'date_registered': int(time.time()),
            'date_last_active': int(time.time()),
        }
        try:
            collection_users.insert_one(user_to_add)
            return True
        except DuplicateKeyError:
            print(f"Duplicate: {self.user_id}")
            return False

    async def update_last_active(self) -> bool:
        try:
            collection_users.update_one(
                {
                    '_id': self.user_id
                },
                {
                    '$set': {
                        "date_last_active": int(time.time())
                    }
                }
            )
            return True
        except:
            return False

    async def update_field(self, field, value):
        collection_users.update_one(
            {
                '_id': self.user_id
            },
            {
                '$set': {
                    field: value
                }
            }
        )
