from utils.api import APIManager
from utils.handler import collect

manager = APIManager()

games_info = manager.get_data(use_net=False)
games_info = collect(games_info, debug=True)
