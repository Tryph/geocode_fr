from django.contrib.gis import admin

from .models import Address, Department, Municipality, Region, Way, ZipCode

admin.site.register(Address, admin.GeoModelAdmin)
admin.site.register(Department, admin.GeoModelAdmin)
admin.site.register(Municipality, admin.GeoModelAdmin)
admin.site.register(Region, admin.GeoModelAdmin)
admin.site.register(Way, admin.GeoModelAdmin)
admin.site.register(ZipCode)
