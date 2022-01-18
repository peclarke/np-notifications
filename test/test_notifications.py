from typing import List
import pytest
from consts import StatusCode
from unittest import mock
from data.Fleet import Fleet
from main import NeptunesPrideStatus
from notifications import format_message

def mock_send_message(message, np: NeptunesPrideStatus):
    return True

def mock_failed_message(message, np: NeptunesPrideStatus):
    return False

def test_enemy_format_message(status: NeptunesPrideStatus, fleet_one: Fleet):
    enemies: List[Fleet] = [fleet_one]

    with mock.patch("notifications.send_message", wraps=mock_send_message):
        res = format_message(StatusCode.ENEMY, enemies, status)
        assert res[0] == 200
        assert res[1] == "Message sent!"

def test_failed_format(status: NeptunesPrideStatus, fleet_one: Fleet):
    enemies: List[Fleet] = [fleet_one]

    with mock.patch("notifications.send_message", wraps=mock_failed_message):
        res = format_message(StatusCode.ENEMY, enemies, status)
        assert res[0] == 400
        assert res[1] == "Error"

def test_multiple_enemies(status: NeptunesPrideStatus, fleet_one, fleet_two):
    enemies: List[Fleet] = [fleet_one, fleet_two]

    with mock.patch("notifications.send_message", wraps=mock_send_message):
        res = format_message(StatusCode.ENEMY, enemies, status)
        assert res[0] == 200
        assert res[1] == "Message sent!"

def test_failure_multiple_enemies(status: NeptunesPrideStatus, fleet_one, fleet_two):
    enemies: List[Fleet] = [fleet_one, fleet_two]

    with mock.patch("notifications.send_message", wraps=mock_failed_message):
        res = format_message(StatusCode.ENEMY, enemies, status)
        assert res[0] == 400
        assert res[1] == "Error"

def test_daily_digest(status: NeptunesPrideStatus, fleet_one, fleet_two):
    enemies: List[List[Fleet]] = [[fleet_one], [fleet_two]]

    with mock.patch("notifications.send_message", wraps=mock_send_message):
        res = format_message(StatusCode.DAILY, enemies, status)
        assert res[0] == 200
        assert res[1] == "Message sent!"

def test_failure_daily_digest(status: NeptunesPrideStatus, fleet_one, fleet_two):
    enemies: List[List[Fleet]] = [[fleet_one], [fleet_two]]

    with mock.patch("notifications.send_message", wraps=mock_failed_message):
        res = format_message(StatusCode.DAILY, enemies, status)
        assert res[0] == 400
        assert res[1] == "Error"