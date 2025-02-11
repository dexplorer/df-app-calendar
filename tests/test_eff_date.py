import pytest
from app_calendar import eff_date as ed


def test_get_cur_cycle_date():
    assert ed.get_cur_cycle_date() == "2024-12-26"


test_data = [
    ("2024-12-26", "%Y-%m-%d", True),
    ("2024-12-26", "%Y%m%d", False),
    ("20241226", "%Y-%m-%d", False),
    ("2024-13-26", "%Y-%m-%d", False),
]


@pytest.mark.parametrize("given_date, date_format, expected_ouput", test_data)
def test_check_if_valid_date(given_date: str, date_format: str, expected_ouput: bool):
    assert ed.check_if_valid_date(given_date, date_format) == expected_ouput
