# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from mainsite.system.storage import ImageStorage

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    list1 = models.CharField(max_length=255)
    list2 = models.CharField(max_length=255)
    list3 = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    realname = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user'


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(db_column='ISBN', max_length=100, blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey('Category', models.DO_NOTHING, db_column='categoryid')
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'book'


class Browser(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    num = models.IntegerField()
    lasttime = models.DateTimeField()

    class Meta:
        db_table = 'browser'


class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    address = models.CharField(max_length=255)

    class Meta:
        db_table = 'location'


class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    ordertime = models.DateTimeField()
    status = models.CharField(max_length=255)
    buyer = models.ForeignKey('User', models.DO_NOTHING, db_column='buyer')
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    phonenum = models.CharField(max_length=255, blank=True, null=True)
    finishtime = models.DateTimeField(blank=True, null=True)
    visible = models.CharField(max_length=10)

    class Meta:
        db_table = 'order'


class Orderitem(models.Model):
    orderid = models.ForeignKey(Order, models.DO_NOTHING, db_column='orderid')
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    quantity = models.IntegerField()
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prices = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'orderitem'


class Phone(models.Model):
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    phonenum = models.IntegerField()

    class Meta:
        db_table = 'phone'


class Presale(models.Model):
    id = models.IntegerField(primary_key=True)
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    restnum = models.IntegerField()
    publishtime = models.DateTimeField()
    finishtime = models.DateTimeField()

    class Meta:
        db_table = 'presale'


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='userid')
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    star = models.DecimalField(max_digits=5, decimal_places=2)
    info = models.CharField(max_length=255)
    publishdate = models.DateTimeField()

    class Meta:
        db_table = 'review'


class Storage(models.Model):
    id = models.IntegerField(primary_key=True)
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    purchasetime = models.DateTimeField()
    puchasenum = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prices = models.DecimalField(max_digits=15, decimal_places=2)
    restnum = models.IntegerField()

    class Meta:
        db_table = 'storage'


class Walfare(models.Model):
    id = models.IntegerField(primary_key=True)
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

    class Meta:
        db_table = 'walfare'

class Picture(models.Model):
    id = models.IntegerField(primary_key=True)
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='bookid')
    image = models.ImageField(upload_to='img/%Y/%m/%d',storage=ImageStorage())

    class Meta:
        db_table = 'picture'