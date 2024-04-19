from utils.api import APIManager
from utils.handler import collect

manager = APIManager()

games_info = manager.get_data(use_net=False)
collect(games_info)

