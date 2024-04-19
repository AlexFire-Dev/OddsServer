from OddsServer.celery import app

import time


# test_sum.delay()
@app.task
def test_sum():
    time.sleep(15)
    print(2+2)
