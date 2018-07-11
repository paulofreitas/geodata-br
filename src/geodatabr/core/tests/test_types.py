#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2018 Paulo Freitas
# MIT License (see LICENSE file)
"""Core types testing module."""
# pylint: disable=expression-not-assigned, no-self-use, pointless-statement

# Imports

# External dependencies

import pytest

# Package dependencies

from geodatabr.core import types

# Classes


class TestAbstractClass(object):
    """Tests AbstractClass type methods."""

    def testParents(self):
        """Tests if AbstractClass.parents() method works as expected."""
        # pylint: disable=missing-docstring
        class Foo(types.AbstractClass):
            pass

        class Bar(Foo):
            pass

        assert len(Bar.parents()) == 1
        assert Bar.parents()[0] == Foo

    def testChilds(self):
        """Tests if AbstractClass.childs() method works as expected."""
        # pylint: disable=missing-docstring
        class Foo(types.AbstractClass):
            pass

        class Bar(Foo):
            pass

        assert len(Foo.childs()) == 1
        assert Foo.childs()[0] == Bar


class TestList(object):
    """Tests List type methods."""

    def testAnd(self):
        """Tests if List.__and__() works as expected."""
        numbers = types.List(range(10))
        common_numbers = numbers & types.List(range(5))

        assert isinstance(common_numbers, types.List)
        assert common_numbers == [0, 1, 2, 3, 4]

        with pytest.raises(ValueError):
            numbers & range(5)

    def testChunk(self):
        """Tests if List.chunk() method work as expected."""
        numbers = types.List(range(10))
        number_groups = numbers.chunk(3)

        assert isinstance(number_groups, types.List)
        assert len(number_groups) == 4
        assert number_groups[-1] == [9]
        assert isinstance(number_groups[-1], types.List)

    def testCopy(self):
        """Tests if List.copy() works as expected."""
        numbers = types.List(range(10))

        assert isinstance(numbers.copy(), types.List)
        assert numbers.copy() == numbers

    def testDifference(self):
        """Tests if List.difference() works as expected."""
        numbers = types.List(range(10))
        diff_numbers = numbers.difference(types.List(range(5)))

        assert isinstance(diff_numbers, types.List)
        assert diff_numbers == [5, 6, 7, 8, 9]

        with pytest.raises(ValueError):
            numbers.difference(range(5))

    def testFilter(self):
        """Tests if List.filter() works as expected."""
        numbers = types.List(range(10))
        odd_numbers = numbers.filter(lambda item: not item & 1)

        assert isinstance(odd_numbers, types.List)
        assert odd_numbers == [0, 2, 4, 6, 8]

        with pytest.raises(ValueError):
            numbers.filter(1)

    def testFirst(self):
        """Tests if List.first() works as expected."""
        numbers = types.List(range(10))

        assert numbers.first() == 0
        assert numbers.first(lambda item: not item & 1) == 0

        with pytest.raises(ValueError):
            numbers.first(1)

    def testFlatten(self):
        """Tests if List.flatten() works as expected."""
        number_groups = types.List([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])
        numbers = number_groups.flatten()

        assert isinstance(numbers, types.List)
        assert numbers == types.List(range(10))

    def testIntersection(self):
        """Tests if List.intersection() works as expected."""
        numbers = types.List(range(10))
        common_numbers = numbers.intersection(types.List(range(5)))

        assert isinstance(common_numbers, types.List)
        assert common_numbers == [0, 1, 2, 3, 4]

        with pytest.raises(ValueError):
            numbers.intersection(range(5))

    def testLast(self):
        """Tests if List.last() works as expected."""
        numbers = types.List(range(10))

        assert numbers.last() == 9
        assert numbers.last(lambda item: not item & 1) == 8

        with pytest.raises(ValueError):
            numbers.last(1)

    def testNth(self):
        """Tests if List.nth() works as expected."""
        numbers = types.List(range(10))

        assert isinstance(numbers.nth(3), types.List)
        assert numbers.nth(3) == [0, 3, 6, 9]
        assert numbers.nth(3, 2) == [2, 5, 8]

    def testOr(self):
        """Tests if List.__or__() works as expected."""
        numbers = types.List(range(10))
        unique_numbers = numbers | types.List(range(15))

        assert isinstance(unique_numbers, types.List)
        assert len(unique_numbers) == 15
        assert unique_numbers == types.List(range(15))

        with pytest.raises(ValueError):
            numbers | range(15)

    def testPartition(self):
        """Tests if List.partition() works as expected."""
        numbers = types.List(range(10))
        number_groups = numbers.partition(lambda item: item & 1)

        assert isinstance(number_groups, types.List)
        assert isinstance(number_groups[0], types.List)
        assert number_groups[0] == [1, 3, 5, 7, 9]

        with pytest.raises(ValueError):
            numbers.partition(1)

    def testPreprend(self):
        """Tests if List.prepend() works as expected."""
        numbers = types.List()
        numbers.prepend(1)
        numbers.prepend(0)

        assert numbers[0] == 0
        assert numbers[1] == 1

    def testReduce(self):
        """Tests if List.reduce() works as expected."""
        numbers = types.List(range(10))

        assert numbers.reduce(lambda x, y: x + y, 0) == 45
        assert numbers.reduce(lambda x, y: x - y, 0) == -45
        assert numbers.reduce(lambda x, y: x * y, 0) == 0

        with pytest.raises(ValueError):
            numbers.reduce(1)

    def testReject(self):
        """Tests if List.reject() works as expected."""
        numbers = types.List(range(10))
        odd_numbers = numbers.reject(lambda item: item & 1)

        assert isinstance(odd_numbers, types.List)
        assert odd_numbers == [0, 2, 4, 6, 8]

        with pytest.raises(ValueError):
            numbers.reject(1)

    def testRotate(self):
        """Tests if List.rotate() works as expected."""
        numbers = types.List(range(10))
        rotated_numbers = numbers.rotate(1)

        assert isinstance(rotated_numbers, types.List)
        assert rotated_numbers == [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    def testSample(self):
        """Tests if List.sample() works as expected."""
        numbers = types.List(range(10))

        assert numbers.sample()[0] in numbers
        assert len(numbers.sample(2)) == 2
        assert all(number in numbers for number in numbers.sample(2))
        assert numbers.sample(0) == []

        with pytest.raises(ValueError):
            numbers.sample(-1)

    def testShift(self):
        """Tests if List.shift() works as expected."""
        numbers = types.List(range(10))

        assert numbers.shift() == 0
        assert numbers.shift() == 1

    def testShuffle(self):
        """Tests if List.shuffle() works as expected."""
        numbers = types.List(range(10))
        shuffled_numbers = numbers.shuffle()

        assert isinstance(shuffled_numbers, types.List)
        assert shuffled_numbers != numbers

    def testSplice(self):
        """Tests if List.splice() works as expected."""
        numbers = types.List(range(10))
        sliced_numbers = numbers.splice(5)

        assert isinstance(sliced_numbers, types.List)
        assert sliced_numbers == [5, 6, 7, 8, 9]
        assert numbers == [0, 1, 2, 3, 4]
        assert numbers.splice(1, 3) == [1, 2, 3]
        assert numbers == [0, 4]

    def testSplit(self):
        """Tests if List.split() works as expected."""
        numbers = types.List(range(10))
        number_groups = numbers.split(3)

        assert isinstance(number_groups, types.List)
        assert len(number_groups) == 3
        assert number_groups[0] == [0, 1, 2]
        assert number_groups[-1] == [6, 7, 8, 9]

    def testStringRepresentation(self):
        """Tests if List.__repr__() works as expected."""
        numbers = types.List(range(10))

        assert repr(numbers) == 'List([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])'

    def testSub(self):
        """Tests if List.__sub__() works as expected."""
        numbers = types.List(range(10))
        diff_numbers = numbers - types.List(range(5))

        assert isinstance(diff_numbers, types.List)
        assert diff_numbers == [5, 6, 7, 8, 9]

        with pytest.raises(ValueError):
            numbers - range(5)

    def testTake(self):
        """Tests if List.take() works as expected."""
        numbers = types.List(range(10))
        sliced_numbers = numbers.take(3)

        assert isinstance(sliced_numbers, types.List)
        assert sliced_numbers == [0, 1, 2]

    def testTranspose(self):
        """Tests if List.transpose() works as expected."""
        items = types.List([['x', 'y', 'z'], [0, 1, 2]])
        coords = items.transpose()

        assert isinstance(coords, types.List)
        assert coords == [('x', 0), ('y', 1), ('z', 2)]

        with pytest.raises(ValueError):
            types.List([['x', 'y'], 0]).transpose()

        with pytest.raises(ValueError):
            types.List([['x', 'y'], [0]]).transpose()

    def testUnion(self):
        """Tests if List.union() works as expected."""
        numbers = types.List(range(10))
        unique_numbers = numbers.union(types.List(range(15)))

        assert isinstance(unique_numbers, types.List)
        assert len(unique_numbers) == 15
        assert unique_numbers == types.List(range(15))

        with pytest.raises(ValueError):
            numbers.union(range(15))

    def testUnique(self):
        """Tests if List.unique() works as expected."""
        numbers = types.List([0, 1, 2, 2, 3, 3, 3])
        unique_numbers = numbers.unique()

        assert isinstance(unique_numbers, types.List)
        assert len(unique_numbers) == 4
        assert unique_numbers == [0, 1, 2, 3]


class TestMap(object):
    """Tests Map type methods."""

    def testAttributeAccess(self):
        """Tests if Map.__getattr__() works as expected."""
        coords = types.Map(x=0, y=1)

        assert coords.x == 0 and coords.y == 1

        with pytest.raises(AttributeError):
            coords.z

    def testAttributeAssignment(self):
        """Tests if Map.__setattr__() works as expected."""
        coords = types.Map()
        coords.x = 0
        coords.y = 1

        assert coords.x == 0 and coords.y == 1

    def testAttributeDeletion(self):
        """Tests if Map.__delattr__() works as expected."""
        coords = types.Map(x=0, y=1)

        del coords.x

        with pytest.raises(AttributeError):
            coords.x

    def testStringRepresentation(self):
        """Tests if Map.__repr__() works as expected."""
        coords = types.Map(x=0, y=1)

        assert repr(coords) == 'Map(x=0, y=1)'

    def testCopy(self):
        """Tests if Map.copy() works as expected."""
        coords = types.Map(x=0, y=1)

        assert isinstance(coords.copy(), types.Map)
        assert coords.copy() == coords


class TestString(object):
    """Tests String type methods."""

    def testAfter(self):
        """Tests if String.after() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.after('fox') == ' jumps over the lazy dog'

    def testBefore(self):
        """Tests if String.before() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.before('fox') == 'The quick brown '

    def testDedent(self):
        """Tests if String.dedent() works as expected."""
        sentence = types.String(
            '  The quick brown fox\n  jumps over the lazy dog')

        assert sentence.dedent() \
            == 'The quick brown fox\njumps over the lazy dog'

    def testIndent(self):
        """Tests if String.indent() works as expected."""
        sentence = types.String('The quick brown fox\njumps over the lazy dog')

        assert sentence.indent('  ') \
            == '  The quick brown fox\n  jumps over the lazy dog'

    def testRepeat(self):
        """Tests if String.repeat() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.repeat(3) == sentence * 3

    def testReverse(self):
        """Tests if String.reverse() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.reverse() \
            == 'god yzal eht revo spmuj xof nworb kciuq ehT'

    def testRotate(self):
        """Tests if String.rotate() works as expected."""
        word = types.String('rotate')

        assert word.rotate(4) == 'tatero'
        assert word.rotate(-4) == 'terota'

    def testSentence(self):
        """Tests if String.sentence() works as expected."""
        four_items = ['one', 'two', 'three', 'four']
        two_items = ['one', 'two']

        assert types.String.sentence(four_items) == 'one, two, three, four'
        assert types.String.sentence(four_items, ',') == 'one,two,three,four'
        assert types.String.sentence(four_items, last_delimiter=' and ') \
            == 'one, two, three and four'
        assert types.String.sentence(four_items,
                                     last_delimiter=' and ',
                                     serial=True) == 'one, two, three, and four'
        assert types.String.sentence(two_items,
                                     last_delimiter=' and ',
                                     serial=True) == 'one and two'

    def testTruncate(self):
        """Tests if String.truncate() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.truncate() == sentence
        assert sentence.truncate(20) == 'The quick brown...'
        assert sentence.truncate(20, '…') == 'The quick brown fox…'

    def testWrap(self):
        """Tests if String.wrap() works as expected."""
        sentence = types.String('The quick brown fox jumps over the lazy dog')

        assert sentence.wrap() == sentence
        assert sentence.wrap(20) \
            == 'The quick brown fox\njumps over the lazy\ndog'
