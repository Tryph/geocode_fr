from django.db import models


class DataSource(models.Model):
    class Meta:
        verbose_name = _("data source")
        verbose_name_plural = _("data sources")

    name = models.CharField(max_length=200)
    url = models.CharField(max_length=2048)
    downloaded = models.DateTimeField(null=True)
    processed = models.DateTimeField(null=True)
    inserted = models.DateTimeField(null=True)

