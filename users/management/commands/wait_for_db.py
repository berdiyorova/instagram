import time

from django.core.management import BaseCommand
from django.db.utils import OperationalError
from psycopg2.errors import OperationalError as PsycopgError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database ...")
        db_check = False

        while db_check is False:
            try:
                self.check(databases=["default"])
                db_check = True
            except (PsycopgError, OperationalError):
                self.stdout.write(self.style.ERROR("Database is not ready"))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is ready"))
