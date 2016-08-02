# -*- coding: utf-8 -*-
import sys

default_app_config = 'djcompoundqueryset.apps.CompoundQuerySetConfig'


class CompoundQueryset:
    def __init__(self, *args, **kwargs):
        # Max items will limit the query scope if you know you only need the first X items
        max_items = kwargs.pop('max_items', None)
        assert max_items is None or isinstance(max_items, int)
        self.querysets = args
        self.__counts = None
        self.__max_items = max_items

    def _update_counts(self):
        if self.__counts is None:
            total = 0
            counts = []
            for q in self.querysets:
                if self.__max_items is None:
                    cur_count = q.count()
                else:
                    count_stop_index = self.__max_items - total
                    count_stop_index = max(0, count_stop_index)
                    cur_count = q[:count_stop_index].count()
                total += cur_count
                counts.append(cur_count)
                if self.__max_items is not None and total >= self.__max_items:
                    break
            self.__counts = counts

    def count(self):
        self._update_counts()
        return sum(self.__counts)

    def __len__(self):
        return self.count()

    def __getitem__(self, given):
        self._update_counts()
        result = []
        passed = 0
        if isinstance(given, slice):
            # We have a slice
            target_start = given.start
            if target_start is None:
                target_start = 0
            target_stop = given.stop
            if target_stop is None:
                target_stop = sys.maxsize
            if self.__max_items is not None and target_stop > self.__max_items:
                target_stop = self.__max_items
            for idx, qs in enumerate(self.querysets):
                qs_count = self.__counts[idx]
                start = target_start - passed
                stop = target_stop - passed
                passed += qs_count
                if start < qs_count and stop < qs_count:
                    # We got entire result here
                    result.extend(qs[start:stop])
                    break
                elif start < qs_count:
                    # We got a partial match
                    new_results = qs[start:stop]
                    result.extend(new_results)
                    target_start += len(new_results)
        else:
            # Plain index
            for idx, qs in enumerate(self.querysets):
                qs_count = self.__counts[idx]
                start = given - passed
                passed += qs_count
                if start < qs_count:
                    return qs[start]
            raise IndexError('list index out of range')
        return result
