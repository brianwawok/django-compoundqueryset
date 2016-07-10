# -*- coding: utf-8 -*-

default_app_config = 'djcompoundqueryset.apps.CompoundQuerySetConfig'


class CompoundQueryset:
    def __init__(self, *args):
        self.querysets = args
        self.__counts = None

    def _update_counts(self):
        if self.__counts is None:
            self.__counts = [q.count() for q in self.querysets]

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
            target_stop = given.stop
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
