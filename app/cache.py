import redis
import json
class GameCache:
    def __init__(self, host='redis', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db,decode_responses=True,socket_connect_timeout=3 )
         # Проверка подключения
        self.r.ping()
    
    def save_state(self, game_id,state):
        self.r.set(f"game:{game_id}", json.dumps(state), ex=86400)  # TTL 24 часа

    def load_state(self, game_id):
        data = self.r.get(f"game:{game_id}")
        return json.loads(data) if data else None

# import redis
# import json

# class GameCache:
#     def __init__(self, host='localhost', port=6379, db=0):
#         self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True, socket_connect_timeout=3)
#         # Проверка подключения
#         self.r.ping()
    
#     def save_game_state(self, game_id, name1, name2, state):
#         """Сохранить состояние игры с именами игроков"""
#         game_data = {
#             'players': {'name1': name1, 'name2': name2},
#             'state': state
#         }
#         self.r.set(f"game:{game_id}", json.dumps(game_data), ex=86400)  # TTL 24 часа
    
#     def load_game_state(self, game_id):
#         """Загрузить состояние игры с именами игроков"""
#         data = self.r.get(f"game:{game_id}")
#         if data:
#             game_data = json.loads(data)
#             return game_data['players'], game_data['state']
#         return None, None
    
#     def save_player_names(self, name1, name2):
#         """Сохранить имена игроков отдельно (для автозаполнения)"""
#         players_data = {'name1': name1, 'name2': name2}
#         self.r.set("player_names", json.dumps(players_data), ex=2592000)  # TTL 30 дней
    
#     def load_player_names(self):
#         """Загрузить последние использованные имена игроков"""
#         data = self.r.get("player_names")
#         if data:
#             players_data = json.loads(data)
#             return players_data.get('name1', 'Игрок 1'), players_data.get('name2', 'Игрок 2')
#         return "Игрок 1", "Игрок 2"
    
#     def save_state(self, key, data):
#         """Универсальный метод сохранения (для обратной совместимости)"""
#         self.r.set(key, json.dumps(data), ex=86400)
    
#     def load_state(self, key):
#         """Универсальный метод загрузки (для обратной совместимости)"""
#         data = self.r.get(key)
#         return json.loads(data) if data else None