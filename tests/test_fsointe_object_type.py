import pytest
from pytest_mock import mocker

from path import Path

from fsops.fso import Type
from fsops.fso.exceptions import FSOTypeException

def test_type_isfile(mocker):
    fso_path = Path('test')

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isfile.return_value = True

    assert Type.from_path(fso_path).is_file is True
    assert Type.from_path(fso_path).is_dir is False
    assert Type.from_path(fso_path).is_link is False


def test_type_isdir(mocker):
    fso_path = Path('test')

    mock_path_isfile = mocker.patch.object(fso_path, "isdir")
    mock_path_isfile.return_value = True

    assert Type.from_path(fso_path).is_file is False
    assert Type.from_path(fso_path).is_dir is True
    assert Type.from_path(fso_path).is_link is False


def test_type_islink(mocker):
    fso_path = Path('test')

    mock_path_isfile = mocker.patch.object(fso_path, "islink")
    mock_path_isfile.return_value = True

    assert Type.from_path(fso_path).is_file is False
    assert Type.from_path(fso_path).is_dir is False
    assert Type.from_path(fso_path).is_link is True


@pytest.mark.parametrize("isfile", [
    True
])
@pytest.mark.parametrize("isdir", [
    False,
    True
])
@pytest.mark.parametrize("islink", [
    True
])
def test_type_raise_exception(mocker, isfile, isdir, islink):
    fso_path = Path('test')

    mock_path_isfile = mocker.patch.object(fso_path, "isfile")
    mock_path_isdir = mocker.patch.object(fso_path, "isdir")
    mock_path_islink = mocker.patch.object(fso_path, "islink")
    mock_path_isfile.return_value = isfile
    mock_path_isdir.return_value = isdir
    mock_path_islink.return_value = islink

    with pytest.raises(FSOTypeException) as excinfo:
        Type.from_path(fso_path)
    assert excinfo.value.message == 'File can only be of one type'

