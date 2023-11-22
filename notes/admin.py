from django.contrib import admin

from notes.models import Trade
from notes.models import Asset
from notes.models import Trigger


admin.site.register(Trade)
admin.site.register(Asset)
admin.site.register(Trigger)
