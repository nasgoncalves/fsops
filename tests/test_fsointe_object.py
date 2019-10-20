import pytest
import os
from pytest_mock import mocker

from path import Path

from fsops.fso import Object
from fsops.fso import Hash
from fsops.fso import MetaType
from fsops.fso import Time
from fsops.fso import Type

from os import stat_result

from datetime import datetime
import pytz
import hashlib

# def test_object_init_path(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.path == os.path.normpath('{}/test.txt'.format(
#         os.path.dirname(os.path.realpath(__file__))))


# def test_object_init_name(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.name == 'test.txt'


# def test_object_init_ext(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.ext == '.txt'


# def test_object_init_hash(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     hash_object = hashlib.sha512('data')
#     hex_dig = hash_object.hexdigest()

#     assert fso.hash.sha512 == hex_dig


# def test_object_init_size(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.size == len('data')


# def test_object_init_type(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.type.is_file == True
#     assert fso.type.is_dir == False
#     assert fso.type.is_link == False


# # def test_object_init_time(mocker, file_system_object):
# #     fso = Object.from_path(file_system_object)

# #     utc_create = Time.string_to_datetime(fso.time.creation)
# #     utc_modified = Time.string_to_datetime(fso.time.modified)

# #     utc_create = utc_create.replace(tzinfo=pytz.utc)
# #     utc_modified = utc_modified.replace(tzinfo=pytz.utc)

# #     assert str(utc_create) == "2015-10-25 00:41:13+00:00"
# #     assert str(utc_modified) == "2018-12-25 09:27:53+00:00"


# def test_object_init_mode(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.mode == '0644'


# def test_object_init_metatype(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)

#     assert fso.meta.mimetype == 'text/plain'
#     assert fso.meta.binary == False
#     assert fso.meta.link == ''


# def test_object_init_from_path_error(mocker, file_system_object):
#     with pytest.raises(Exception):
#         Object.from_path('doesnt_exist')


# def test_hash_str(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert str(fso.hash) == "Hash(sha512='77c7ce9a5d86bb386d443bb96390faa120633158699c8844c30b13ab0bf92760b7e4416aea397db91b4ac0e5dd56b8ef7e4b066162ab1fdc088319ce6defc876')"


# def test_hash_eval(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert fso.hash == eval(
#         "Hash(sha512='77c7ce9a5d86bb386d443bb96390faa120633158699c8844c30b13ab0bf92760b7e4416aea397db91b4ac0e5dd56b8ef7e4b066162ab1fdc088319ce6defc876')")


# def test_meta_str(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert str(
#         fso.meta) == "MetaType(mimetype='text/plain', binary=False, link='')"


# def test_meta_eval(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert fso.meta == eval(
#         "MetaType(mimetype='text/plain', binary=False, link='')")


# # def test_time_str(mocker, file_system_object):
# #     fso = Object.from_path(file_system_object)
# #     assert str(
# #         fso.time) == "Time(creation='2015-10-25 00:41:13', modified='2018-12-25 09:27:53')"


# # def test_time_eval(mocker, file_system_object):
# #     fso = Object.from_path(file_system_object)
# #     assert fso.time == eval(
# #         "Time(creation='2015-10-25 00:41:13', modified='2018-12-25 09:27:53')")


# def test_type_str(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert str(
#         fso.type) == "Type(is_file=True, is_dir=False, is_link=False)"


# def test_type_eval(mocker, file_system_object):
#     fso = Object.from_path(file_system_object)
#     assert fso.type == eval(
#         "Type(is_file=True, is_dir=False, is_link=False)")
