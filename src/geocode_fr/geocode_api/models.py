from django.contrib.gis.db import models
from django.contrib.gis.db.models import PolygonField, PointField
from django.contrib.postgres import search
from django.utils.translation import ugettext_lazy as _


class Region(models.Model):
    class Meta:
        verbose_name = _("region")
        verbose_name_plural = _("regions")

    cog = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)
    vectorized = search.SearchVectorField(null=True)
    capital = models.ForeignKey('Municipality', on_delete=models.PROTECT,
                                related_name='reg_cap_id', null=True)
    geometry_simple = PolygonField(null=True, geography=True)
    geometry_medium = PolygonField(null=True, geography=True)
    geometry_detail = PolygonField(null=True, geography=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")

    cog = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=200)
    vectorized = search.SearchVectorField(null=True)
    capital = models.ForeignKey('Municipality', on_delete=models.PROTECT,
                                related_name='dep_cap_id', null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    geometry_simple = PolygonField(null=True, geography=True)
    geometry_medium = PolygonField(null=True, geography=True)
    geometry_detail = PolygonField(null=True, geography=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    class Meta:
        verbose_name = _("municipality")
        verbose_name_plural = _("municipalities")

    cog = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=200)
    vectorized = search.SearchVectorField(null=True)
    position = PointField(null=True, geography=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    geometry_simple = PolygonField(null=True, geography=True)
    geometry_medium = PolygonField(null=True, geography=True)
    geometry_detail = PolygonField(null=True, geography=True)

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    class Meta:
        verbose_name = _("zipcode")
        verbose_name_plural = _("zipcodes")

    code = models.CharField(max_length=5, primary_key=True)
    municipalities = models.ManyToManyField(Municipality)

    def __str__(self):
        return self.code


class Way(models.Model):
    class Meta:
        verbose_name = _("way")
        verbose_name_plural = _("ways")

    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, null=True)
    vectorized = search.SearchVectorField(null=True)
    position = PointField(null=True, geography=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    way = models.ForeignKey(Way, on_delete=models.PROTECT)
    number = models.CharField(max_length=20)
    repetition = models.CharField(max_length=20, null=True)
    position = PointField(null=True, geography=True)

    def __str__(self):
        return self.number
