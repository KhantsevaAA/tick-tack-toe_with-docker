import redis
import json
class GameCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db,decode_responses=True,socket_connect_timeout=3 )
         # Проверка подключения
        self.r.ping()
    
    def save_state(self, game_id,name1,name2,state):
        self.r.set(f"game:{game_id}", f"players:{name1, name2}", json.dumps(state), ex=86400)  # TTL 24 часа

    def load_state(self, game_id):
        data = self.r.get(f"game:{game_id}")
        return json.loads(data) if data else None

# import redis

# # Подключение с обработкой ошибок
# try:
#     r = redis.Redis(
#         host='redis',
#         port=6379,
#         db=0,
#         decode_responses=True,
#         socket_connect_timeout=3  # Таймаут 3 секунды
#     )
   
#     print(r.ping())
   
# except redis.ConnectionError as e:
#     print(f"Ошибка подключения: {e}")   
    