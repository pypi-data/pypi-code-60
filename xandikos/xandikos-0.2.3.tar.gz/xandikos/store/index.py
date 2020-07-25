# Xandikos
# Copyright (C) 2019 Jelmer Vernooĳ <jelmer@jelmer.uk>, et al.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 3
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Indexing.
"""

import collections
import logging


INDEXING_THRESHOLD = 5


class Index(object):
    """Index management."""

    def available_keys(self):
        """Return list of available index keys."""
        raise NotImplementedError(self.available_indexes)

    def get_values(self, name, etag, keys):
        """Get the values for specified keys for a name."""
        raise NotImplementedError(self.get_values)

    def iter_etags(self):
        """Return all the etags covered by this index."""
        raise NotImplementedError(self.iter_etags)


class MemoryIndex(Index):

    def __init__(self):
        self._indexes = {}
        self._in_index = set()

    def available_keys(self):
        return self._indexes.keys()

    def get_values(self, name, etag, keys):
        if etag not in self._in_index:
            raise KeyError(etag)
        indexes = {}
        for k in keys:
            if k not in self._indexes:
                raise AssertionError
            try:
                indexes[k] = self._indexes[k][etag]
            except KeyError:
                indexes[k] = []
        return indexes

    def iter_etags(self):
        return iter(self._in_index)

    def add_values(self, name, etag, values):
        for k, v in values.items():
            if k not in self._indexes:
                raise AssertionError
            self._indexes[k][etag] = v
        self._in_index.add(etag)

    def reset(self, keys):
        self._in_index = set()
        self._indexes = {}
        for key in keys:
            self._indexes[key] = {}


class IndexManager(object):

    def __init__(self, index, threshold=INDEXING_THRESHOLD):
        self.index = index
        self.desired = collections.defaultdict(lambda: 0)
        self.indexing_threshold = threshold

    def find_present_keys(self, necessary_keys):
        available_keys = self.index.available_keys()
        needed_keys = []
        missing_keys = []
        new_index_keys = set()
        for keys in necessary_keys:
            found = False
            for key in keys:
                if key in available_keys:
                    needed_keys.append(key)
                    found = True
            if not found:
                for key in keys:
                    self.desired[key] += 1
                    if self.desired[key] > self.indexing_threshold:
                        new_index_keys.add(key)
                missing_keys.extend(keys)
        if not missing_keys:
            return needed_keys

        if new_index_keys:
            logging.debug('Adding new index keys: %r', new_index_keys)
            self.index.reset(
                set(self.index.available_keys()) | new_index_keys)

        # TODO(jelmer): Maybe best to check if missing_keys are satisfiable
        # now?

        return None
