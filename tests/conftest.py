import pytest
import os
import shutil

from path import Path

from os import stat_result

import hashlib

@pytest.fixture
def file_system_object(mocker):
    fso_path = Path('test.txt')

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isfile.return_value = True

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = False

    data = 'data'

    hash_object = hashlib.sha512(data)
    hex_dig = hash_object.hexdigest()

    mock_path_read_hexhash = mocker.patch.object(fso_path, "read_hexhash")
    mock_path_read_hexhash.return_value = hex_dig

    mock_open_file = mocker.mock_open(read_data=data)
    mock_open = mocker.patch("__builtin__.open", mock_open_file)

    mock_path_getsize = mocker.patch.object(fso_path, "getsize")
    mock_path_getsize.return_value = len(data)

    mock_path_stat = mocker.patch("os.stat")
    mock_path_stat.return_value = stat_result((
        0644, 0, 0, 0, 0, 0, 1, 0, 1545730073, 1445730073))

    mock_open_file = mocker.mock_open(read_data=data)
    mock_open = mocker.patch("io.open", mock_open_file)

    return fso_path
