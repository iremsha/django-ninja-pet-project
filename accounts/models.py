from django.db import models
from django.db.models import Model, CharField, IntegerField, FloatField, BooleanField, ForeignKey, CASCADE, DO_NOTHING,\
    ManyToManyField


class Uuid(Model):
    name = CharField(max_length=45, unique=True)


class Name(Model):
    name = CharField(max_length=40, unique=True)


class Balance(Model):
    name = IntegerField(default=0)


class Hold(Model):
    name = IntegerField(default=0)


class Status(Model):
    name = BooleanField(default=False)


class Ad(Model):
    uuid = CharField(max_length=45)
    name = CharField(max_length=45)
    balance = IntegerField(default=0)
    hold = IntegerField(default=0)
    status = BooleanField(default=False)

