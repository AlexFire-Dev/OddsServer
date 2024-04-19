from django.db import models


class OddData(models.Model):
    game_id = models.IntegerField()
    time = models.DateTimeField()
    league_name = models.CharField(max_length=64, null=True, blank=True)
    league_id = models.IntegerField()
    home = models.CharField(max_length=42, null=True, blank=True)
    away = models.CharField(max_length=42, null=True, blank=True)
    date = models.DateField()
    bookmaker = models.CharField(max_length=32)

    home_od = models.FloatField()
    away_od = models.FloatField()
    od_add_time = models.DateTimeField()

    stamp = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.stamp
