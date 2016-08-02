# -*- coding: utf-8 -*-
"""
Created on July 11, 2016

@author: bwawok@gmail.com
"""
from __future__ import absolute_import
from django.core.paginator import Paginator
from django.test import TestCase

from djcompoundqueryset import CompoundQueryset
from .testapp.models import FirstModel, SecondModel


class LoginLogoutTest(TestCase):
    def setUp(self):
        for x in range(0, 10):
            FirstModel.objects.create(age=x, name='namey-' + str(x), color='colory-' + str(x))
            SecondModel.objects.create(age=50 + x, name='other-namey-' + str(x), size=x + 100)

    def test_even_pagination(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)

        p = Paginator(cqs, 2)
        self.assertEqual(10, p.num_pages)
        for page_num in range(1, 10):
            page = p.page(page_num)
            self.assertEqual(2, len(page))
            item_1 = page[0]
            item_2 = page[1]
            if page_num <= 5:
                self.assertEqual(page_num * 2 - 2, item_1.age)
                self.assertEqual(page_num * 2 - 1, item_2.age)
                self.assertIsInstance(item_1, FirstModel)
                self.assertIsInstance(item_2, FirstModel)
            else:
                self.assertEqual((page_num - 5) * 2 + 48, item_1.age)
                self.assertEqual((page_num - 5) * 2 + 49, item_2.age)
                self.assertIsInstance(item_1, SecondModel)
                self.assertIsInstance(item_2, SecondModel)

    def test_split_pagination(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)

        p = Paginator(cqs, 8)
        self.assertEqual(3, p.num_pages)
        page_1 = p.page(1)
        self.assertTrue(all(isinstance(x, FirstModel) for x in page_1))

        page_2 = p.page(2)
        self.assertTrue(isinstance(page_2[0], FirstModel))
        self.assertEqual(8, page_2[0].age)
        self.assertTrue(isinstance(page_2[1], FirstModel))
        self.assertEqual(9, page_2[1].age)
        self.assertTrue(isinstance(page_2[2], SecondModel))
        self.assertEqual(50, page_2[2].age)
        self.assertTrue(isinstance(page_2[3], SecondModel))
        self.assertEqual(51, page_2[3].age)
        self.assertTrue(isinstance(page_2[4], SecondModel))
        self.assertTrue(isinstance(page_2[5], SecondModel))
        self.assertTrue(isinstance(page_2[6], SecondModel))
        self.assertTrue(isinstance(page_2[7], SecondModel))

        page_3 = p.page(3)
        self.assertTrue(all(isinstance(x, SecondModel) for x in page_3))

    def test_individual_access(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)

        self.assertTrue(all(isinstance(cqs[x], FirstModel) for x in range(0, 10)))
        self.assertEqual(0, cqs[0].age)
        self.assertTrue(all(isinstance(cqs[x], SecondModel) for x in range(10, 20)))
        self.assertEqual(50, cqs[10].age)

        try:
            result = cqs[20]
            self.fail()
        except IndexError:
            pass

    def test_iteration(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)

        x = 0
        for i in cqs:
            x += 1

        self.assertEqual(20, x)

    def test_even_pagination_with_big_slice(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)[:1000]

        p = Paginator(cqs, 2)
        self.assertEqual(10, p.num_pages)
        for page_num in range(1, 10):
            page = p.page(page_num)
            self.assertEqual(2, len(page))
            item_1 = page[0]
            item_2 = page[1]
            if page_num <= 5:
                self.assertEqual(page_num * 2 - 2, item_1.age)
                self.assertEqual(page_num * 2 - 1, item_2.age)
                self.assertIsInstance(item_1, FirstModel)
                self.assertIsInstance(item_2, FirstModel)
            else:
                self.assertEqual((page_num - 5) * 2 + 48, item_1.age)
                self.assertEqual((page_num - 5) * 2 + 49, item_2.age)
                self.assertIsInstance(item_1, SecondModel)
                self.assertIsInstance(item_2, SecondModel)

    def test_slice_of_compound(self):
        qs_1 = FirstModel.objects.order_by('age').all()
        qs_2 = SecondModel.objects.order_by('age').all()
        cqs = CompoundQueryset(qs_1, qs_2)[:15]

        p = Paginator(cqs, 2)
        self.assertEqual(8, p.num_pages)
        for page_num in range(1, 8):
            page = p.page(page_num)
            self.assertEqual(2, len(page))
            item_1 = page[0]
            item_2 = page[1]
            if page_num <= 5:
                self.assertEqual(page_num * 2 - 2, item_1.age)
                self.assertEqual(page_num * 2 - 1, item_2.age)
                self.assertIsInstance(item_1, FirstModel)
                self.assertIsInstance(item_2, FirstModel)
            else:
                self.assertEqual((page_num - 5) * 2 + 48, item_1.age)
                self.assertEqual((page_num - 5) * 2 + 49, item_2.age)
                self.assertIsInstance(item_1, SecondModel)
                self.assertIsInstance(item_2, SecondModel)
