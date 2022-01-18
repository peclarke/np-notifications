import pytest
from main import NeptunesPrideStatus

def test_moving_enemies(status: NeptunesPrideStatus):
    res = status.get_moving_enemies()
    assert len(res) == 1
    assert res[0].uid == 14

def test_all_enemies(status: NeptunesPrideStatus):
    res = status.get_enemy_fleets()
    assert len(res) == 2

def test_num_fleets(status: NeptunesPrideStatus):
    assert len(status.fleets) == 3