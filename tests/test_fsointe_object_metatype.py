import pytest
from pytest_mock import mocker

import os
from os import stat_result
from path import Path

from fsops.fso import MetaType
from fsops.fso.exceptions import FSOMetaTypeException


def test_metatype_from_path_isdir(mocker):
    fso_path = Path('test')

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = True

    assert MetaType.is_binary(fso_path) is False

    mock_path_isdir.assert_called_once()


@pytest.mark.parametrize("data,isbinary", [
    ("data", False),
    ("\x01\x02", True),
])
def test_metatype_from_path_isfile_binary(mocker, data, isbinary):
    fso_path = Path('test')

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = False

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isfile.return_value = False

    mock_open_file = mocker.mock_open(read_data=data)
    mock_open = mocker.patch("io.open", mock_open_file)

    assert MetaType.is_binary(fso_path) is isbinary

    mock_path_isdir.assert_called_once()
    mock_open.assert_called()
    mock_open_file.assert_called()


def test_metatype_from_path_dir(mocker):
    fso_path = Path('test')

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = True

    mt = MetaType.from_path(fso_path)

    assert mt.binary == False
    assert mt.mimetype == "inode/directory"
    assert mt.link == ""

    mock_path_isdir.assert_called()


def test_metatype_from_path_link(mocker):
    fso_path = Path('test')

    mock_path_islink = mocker.patch.object(fso_path, "islink")
    mock_path_islink.return_value = True

    mock_path_readlinkabs = mocker.patch.object(fso_path, "readlinkabs")
    mock_path_readlinkabs.return_value = 'abc'

    mt = MetaType.from_path(fso_path)

    assert mt.binary == False
    assert mt.mimetype == 'inode/symlink'
    assert mt.link == 'abc'

    mock_path_islink.assert_called()
