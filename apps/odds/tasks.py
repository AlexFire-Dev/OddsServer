from OddsServer.celery import app
from django.conf import settings

from apps.utils.handler import collect
from apps.utils.api import APIManager
from .models import OddData

from datetime import datetime
import json


def create_db_records(data: list) -> [OddData]:
    result = []
    for record in data:
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
        except KeyError:
            print("Fail")
    return result


@app.task
def update_db():
    """ update_db.delay() """

    print("Requesting data => ", end='')
    try:
        manager = APIManager(
            login=settings.API_LOGIN,
            token=settings.API_TOKEN,
            api_address=settings.API_ADDRESS
        )

        games_info = manager.get_data(use_net=True, forward_days=1)
        games_info = collect(games_info, debug=False)
        print("OK!")

        data_to_add = create_db_records(games_info)
        print(f"Saving {len(data_to_add)} rows => ", end='')
        try:
            OddData.objects.bulk_create(data_to_add, ignore_conflicts=True)
            print("OK!")
        except:
            print("FAIL!")
    except:
        print("FAIL!")
