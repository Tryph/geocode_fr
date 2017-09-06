from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from ...models import DataSource


class Command(BaseCommand):
    help = _("Initilializes the geocoder's data sources table in the database")

    def handle(self, *args, **option):
        pass

