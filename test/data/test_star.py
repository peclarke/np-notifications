from unittest import TestCase
import pytest

from data.Star import Star

def test_is_visibile(star_one: Star, star_two: Star):
    assert not star_one.is_visible()
    assert star_two.is_visible()

def test_invisible_get_points(star_one: Star):
    TestCase().assertDictEqual({}, star_one.get_points())

def test_get_points(star_two: Star):
    TestCase().assertDictEqual({
        'econ': 5,
        'indu': 6,
        'scie': 2
    }, star_two.get_points())