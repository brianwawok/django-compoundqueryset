Django-compoundqueryset
------------

|PyPi|

.. |PyPi| image:: https://badge.fury.io/py/django-compoundqueryset.svg
   :target: https://pypi.python.org/pypi/django-compoundqueryset

A little Django app allows for compound querysets between different tables.
Especially useful for pagination of said results.



Django versions supported: 1.8, 1.9, 1.10

Python versions supported: 2.7, 3.3, 3.4, 3.5



Installation
------------

You can obtain the source code for ``django-compoundqueryset`` from here:

::

    https://github.com/brianwawok/django-compoundqueryset


Using `pip`:

    pip install django-compoundqueryset

Motivation
-----------

Sometimes you might want to combine two different tables with similar fields and show them to users. For example:

.. code:: python

        from django.db import models



        class FirstModel(models.Model):
            age = models.IntegerField()
            name = models.TextField(max_length=100)
            color = models.TextField(max_length=100)


        class SecondModel(models.Model):
            age = models.IntegerField()
            name = models.TextField(max_length=100)
            size = models.IntegerField()


And you want to paginate across them

.. code:: python

        from django.core.paginator import Paginator
        from djcompoundqueryset import CompoundQueryset


        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        combined_queryset = qs_1 | qs_2

        p = Paginator(combined_queryset, 10)

You will get the dreaded error

    Merging 'QuerySet' classes must involve the same values in each case.

Now with django-compoundqueryset, you can do:

.. code:: python

        from django.core.paginator import Paginator
        from djcompoundqueryset import CompoundQueryset


        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        combined_queryset = CompoundQueryset(qs_1, qs_2)

        p = Paginator(combined_queryset, 10)

You can now iterate over these models in a view, showing the age.
