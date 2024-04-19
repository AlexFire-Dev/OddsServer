import datetime
from pytz import timezone


def collect(games_info, debug: bool = False):
    all_games: list = list()
    for game in games_info:
        if game["status"] == 200 and game["success"]:
            tz = timezone('Europe/Moscow')

            info: dict = dict()
            info["game_id"] = int(game["game_id"])
            info["time"] = datetime.datetime.fromtimestamp(int(game["time"]), tz=tz)
            info["league"] = game["league"]["name"]
            info["league_id"] = int(game["league"]["id"])
            info["home"] = game["home"]["name"]
            info["away"] = game["away"]["name"]
            info["date"] = datetime.datetime.strptime(game["date"], "%d.%m.%Y").date()
            # print(game)
            res: dict = game["results"]
            # bookmakers: set = set()
            for key in res.keys():
                info_game = info
                info_game["bookmaker"] = key
                # bookmakers.add(key)
                odds_update = dict()
                odds_update = res[key]["odds_update"]
                odds: list = list()
                for key_2 in odds_update.keys():
                    odds.append(key_2)
                for i in odds:
                    if i == "151_1" and len(res[key]["odds"]["end"]) != 0:
                        # print(res[key]["odds"]["start"])
                        # print(res[key]["odds"]["start"][i])
                        info_game[f"{i}_home_od"] = float(res[key]["odds"]["start"][i]["home_od"])
                        info_game[f"{i}_away_od"] = float(res[key]["odds"]["start"][i]["away_od"])
                        info_game[f"{i}_add_time"] = datetime.datetime.fromtimestamp(int(res[key]["odds"]["start"][i]["add_time"]), tz=tz)
                if "151_1_add_time" not in info_game.keys():
                    break
                else:
                    if debug:
                        print(info_game)
                    all_games.append(info_game)
                    break

    return all_games
    # info["bookmaker"] = bookmakers
