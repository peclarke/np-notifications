import pytest
from data.Fleet import Fleet
from main import NeptunesPrideStatus

def test_is_id_owner_of(fleet_three: Fleet, fleet_two: Fleet, fleet_one: Fleet):
    assert fleet_three.is_id_owner_of(4)
    assert fleet_two.is_id_owner_of(1)
    assert fleet_one.is_id_owner_of(3)

def test_id_is_not_owner_of(fleet_three: Fleet, fleet_two: Fleet, fleet_one: Fleet):
    assert not fleet_three.is_id_owner_of(12)
    assert not fleet_two.is_id_owner_of(3)
    assert not fleet_one.is_id_owner_of(1)