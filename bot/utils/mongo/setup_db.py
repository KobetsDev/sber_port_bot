from pymongo import MongoClient
from data.config import DB_URL

client = MongoClient(DB_URL)
db_name = 'tg_oso'
db = client[db_name]

col_users_name = 'users'
collection_users = db[col_users_name]

col_events_name = 'events'
collection_events = db[col_events_name]

col_orders_name = 'orders'
collection_orders = db[col_orders_name]
