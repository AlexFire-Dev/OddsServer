from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Updating API data'

    def handle(self, *args, **options):
        from apps.odds.tasks import update_db

        update_db()
