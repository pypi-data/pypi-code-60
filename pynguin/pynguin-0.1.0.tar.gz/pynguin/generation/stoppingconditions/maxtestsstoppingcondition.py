# This file is part of Pynguin.
#
# Pynguin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pynguin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pynguin.  If not, see <https://www.gnu.org/licenses/>.
"""A stopping condition that checks the maximum number of test cases."""
import pynguin.configuration as config
from pynguin.generation.stoppingconditions.stoppingcondition import StoppingCondition


class MaxTestsStoppingCondition(StoppingCondition):
    """A stopping condition that checks the maximum number of test cases."""

    def __init__(self):
        self._num_tests = 0
        self._max_tests = config.INSTANCE.search_budget

    def limit(self) -> int:
        return self._max_tests

    def is_fulfilled(self) -> bool:
        return self._num_tests >= self._max_tests

    def reset(self) -> None:
        self._num_tests = 0

    def set_limit(self, limit: int) -> None:
        self._max_tests = limit

    def iterate(self) -> None:
        self._num_tests += 1
