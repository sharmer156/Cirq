# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc
from typing import Any, Union, TYPE_CHECKING

from cirq import value
from cirq.ops import common_gates, eigen_gate

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Tuple


class Pauli(eigen_gate.EigenGate, metaclass=abc.ABCMeta):
    """Represents the Pauli gates.

    This is an abstract class with no public subclasses. The only instances
    of private subclasses are the X, Y, or Z Pauli gates defined below.
    """
    _XYZ = None  # type: Tuple[Pauli, Pauli, Pauli]

    @staticmethod
    def by_index(index: int) -> 'Pauli':
        return Pauli._XYZ[index % 3]

    @staticmethod
    def by_relative_index(p: 'Pauli', relative_index: int) -> 'Pauli':
        return Pauli._XYZ[(p._index + relative_index) % 3]

    def __init__(self, index: int, name: str) -> None:
        self._index = index
        self._name = name

    def commutes_with(self, other: 'Pauli') -> bool:
        return self is other

    def third(self, second: 'Pauli') -> 'Pauli':
        return Pauli._XYZ[(-self._index - second._index) % 3]

    def relative_index(self, second: 'Pauli') -> int:
        """Relative index of self w.r.t. second in the (X, Y, Z) cycle."""
        return (self._index - second._index + 1) % 3 - 1

    def __gt__(self, other):
        if not isinstance(other, Pauli):
            return NotImplemented
        return (self._index - other._index) % 3 == 1

    def __lt__(self, other):
        if not isinstance(other, Pauli):
            return NotImplemented
        return (other._index - self._index) % 3 == 1


class _PauliX(Pauli, common_gates.XPowGate):
    def __init__(self, *, exponent: Union[value.Symbol, float] = 1.0):
        Pauli.__init__(self, index=0, name='X')
        common_gates.XPowGate.__init__(self, exponent=exponent)


class _PauliY(Pauli, common_gates.YPowGate):
    def __init__(self, *, exponent: Union[value.Symbol, float] = 1.0):
        Pauli.__init__(self, index=1, name='Y')
        common_gates.YPowGate.__init__(self, exponent=exponent)


class _PauliZ(Pauli, common_gates.ZPowGate):
    def __init__(self, *, exponent: Union[value.Symbol, float] = 1.0):
        Pauli.__init__(self, index=2, name='Z')
        common_gates.ZPowGate.__init__(self, exponent=exponent)


# The Pauli X gate.
#
# Matrix:
#
#   [[0, 1],
#    [1, 0]]
X = _PauliX()


# The Pauli Y gate.
#
# Matrix:
#
#     [[0, -i],
#      [i, 0]]
Y = _PauliY()


# The Pauli Z gate.
#
# Matrix:
#
#     [[1, 0],
#      [0, -1]]
Z = _PauliZ()


Pauli._XYZ = (X, Y, Z)
