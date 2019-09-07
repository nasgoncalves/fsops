import pytest
from pytest_mock import mocker

import os
from os import stat_result
from path import Path

from datetime import datetime
import pytz

from fsops.fso import Time
from fsops.fso.exceptions import FSOTimeException


@pytest.mark.parametrize("ts,datetime", [
    (1545730073, "2018-12-25 09:27:53"),
    pytest.param(1545730073, "2018-12-25 09:00:53", marks=pytest.mark.xfail)
])
def test_time_datetime_to_string(ts, datetime):
    assert Time.datetime_to_string(ts) == datetime

def test_time_datetime_to_string_exception():
    with pytest.raises(FSOTimeException) as excinfo:
        Time.datetime_to_string("ahahah")
    assert excinfo.value.message == 'Not a valid timestamp (datetime_to_string)'


@pytest.mark.parametrize("datetime_str,ts", [
    ("2018-12-25 09:27:53", 1545730073),
    pytest.param("2018-12-25 a 09:00:53", 1545730073, marks=pytest.mark.xfail)
])
def test_time_string_to_datetime(datetime_str, ts):
    assert Time.string_to_datetime(datetime_str) is not None


def test_time_string_to_datetime_exception():
    with pytest.raises(FSOTimeException) as excinfo:
        Time.string_to_datetime("ahahah")
    assert excinfo.value.message == 'Not a valid timestamp (string_to_datetime)'


# def test_time_from_path(mocker):
#     fso_path = Path('test')

#     mock_path_stat = mocker.patch("os.stat")
#     mock_path_stat.return_value = stat_result((
#         0644, 0, 0, 0, 0, 0, 1, 0, 1545730073, 1445730073))

#     t = Time.from_path(fso_path)

#     utc_create = Time.string_to_datetime(t.creation)
#     utc_modified = Time.string_to_datetime(t.modified)

#     utc_create = utc_create.replace(tzinfo=pytz.utc)
#     utc_modified = utc_modified.replace(tzinfo=pytz.utc)

#     assert str(utc_create) == "2015-10-25 00:41:13+00:00"
#     assert str(utc_modified) == "2018-12-25 09:27:53+00:00"
