import pytest
from pytest_mock import mocker

from path import Path

from fsops.fso import Hash
from fsops.fso import Object
from fsops.fso.exceptions import FSOHashException

def test_hash_init():
    new_hash = Hash(sha512="1" * 128)
    assert len(new_hash.sha512) == 128
    assert new_hash.sha512 == "1" * 128


def test_hash_validation():
    with pytest.raises(FSOHashException) as excinfo:
        Hash(sha512="1")
    assert excinfo.value.message == 'Not a valid SHA512 hash'


def test_hash_file(mocker):
    fso_path = Path('test')

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isfile.return_value = True

    mock_path_read_hexhash = mocker.patch.object(fso_path, "read_hexhash")
    mock_path_read_hexhash.return_value = "1" * 128

    assert Hash.from_path(fso_path).sha512 == "1" * 128
    mock_path_read_hexhash.assert_called_once()
    mock_path_isfile.assert_called_once()


def test_hash_dir(mocker):
    fso_path = Path('test')

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = True

    mock_path_files = mocker.patch.object(fso_path, "files")
    mock_path_files.return_value = ['file1']

    mock_open_file = mocker.mock_open(read_data='data')
    mock_open = mocker.patch("__builtin__.open", mock_open_file)

    hash_dir = Hash.from_path(fso_path)

    mock_path_isdir.assert_called_once()
    mock_path_files.assert_called()
    mock_open.assert_called()
    mock_open_file.assert_called()

    import hashlib
    hash_sha512 = hashlib.sha512()
    hash_sha512.update('data')

    assert hash_dir.sha512 == hash_sha512.hexdigest()


def test_hash_not_recognized_fso_type(mocker):
    fso_path = Path('test')

    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_isdir.return_value = False

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isfile.return_value = False

    with pytest.raises(FSOHashException) as excinfo:
        Hash.from_path(fso_path)
    assert excinfo.value.message == 'FileSystem object not recognized'
