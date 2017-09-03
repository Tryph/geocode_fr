from django.contrib.gis.db import models
from django.contrib.gis.forms.fields import PointField, PolygonField
from django.contrib.postgres import search

from drf_extra_fields.geo_fields import PointField


class Region(models.Model):
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
    code = models.CharField(max_length=5, primary_key=True)
    municipalities = models.ManyToManyField(Municipality)

    def __str__(self):
        return self.code


class Way(models.Model):
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, null=True)
    vectorized = search.SearchVectorField(null=True)
    position = PointField(null=True, geography=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    way = models.ForeignKey(Way, on_delete=models.PROTECT)
    number = models.CharField(max_length=20)
    repetition = models.CharField(max_length=20, null=True)
    position = PointField(null=True, geography=True)

    def __str__(self):
        return self.number
