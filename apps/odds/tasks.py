from OddsServer.celery import app

from apps.utils.handler import collect
from apps.utils.api import APIManager
from .models import OddData

from datetime import datetime
import json


def create_db_records(data: list) -> [OddData]:
    result = []
    for record in data:
        # print(record)
        try:
            result.append(OddData(
                game_id=record["game_id"],
                time=record["time"],
                league_name=record["league"],
                league_id=record["league_id"],
                home=record["home"],
                away=record["away"],
                date=record["date"],
                bookmaker=record["bookmaker"],
                home_od=record["151_1_home_od"],
                away_od=record["151_1_away_od"],
                od_add_time=record["151_1_add_time"],
                stamp=f'{record["bookmaker"]}_{record["game_id"]}_{datetime.timestamp(record["151_1_add_time"])}'
            ))

            # print(f'{record["bookmaker"]}_{record["game_id"]}_{datetime.timestamp(record["151_1_add_time"])}')
        except KeyError:
            print("Fail")
    return result


@app.task
def update_db():
    manager = APIManager()
    games_info = manager.get_data(use_net=False)
    games_info = collect(games_info, debug=False)

    data_to_add = create_db_records(games_info)
    print("Records to add:", len(data_to_add))

    OddData.objects.bulk_create(data_to_add, ignore_conflicts=True)


# test_sum.delay()
@app.task
def test_sum():
    print(2+2)
