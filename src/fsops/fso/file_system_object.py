import mimetypes
from datetime import datetime

import magic
import attr
from attr.validators import instance_of

from .hash import Hash
from .object_base import ObjectBase
from .exceptions import FSOTypeException
from .exceptions import FSOTimeException


@attr.s(frozen=True)
class Type(ObjectBase):
    is_file = attr.ib(validator=instance_of(bool))
    is_dir = attr.ib(validator=instance_of(bool))
    is_link = attr.ib(validator=instance_of(bool))

    @is_file.default
    def make_is_file(self):
        return self.is_file

    @is_dir.default
    def make_is_dir(self):
        return self.is_dir

    @is_link.default
    def make_islink(self):
        return self.is_link

    @classmethod
    def from_path(cls, path):
        if sum([path.isfile(), path.isdir()]) != 1:
            raise FSOTypeException('File can only be of one type')

        return Type(path.isfile(), path.isdir(), path.islink())


@attr.s(frozen=True)
class Time(ObjectBase):
    """
    TimeMetadata class. Holds time data.
    """
    # access = attr.ib(validator=instance_of(str))
    creation = attr.ib(validator=instance_of(str))
    modified = attr.ib(validator=instance_of(str))

    #@access.validator
    @creation.validator
    @modified.validator
    def _validate_modified(self, attribute, value):
        """
        Validate/Verifies if time string id well formmated.

        Arguments:
            attribute {str} -- field name
            value {str} -- field value

        Returns:
            bool -- If date as the correct format will return True
                    else return False.
        """
        return Time.string_to_datetime(value)

    @classmethod
    def string_to_datetime(cls, str_dt):
        """
        Converts string to datetime.

        Arguments:
            str_dt {str} -- Datetime string

        Returns:
            datetime -- Datetime equivalent to the string
        """

        try:
            return datetime.strptime(str_dt, '%Y-%m-%d %H:%M:%S')
        except Exception:
            raise FSOTimeException(
                'Not a valid timestamp (string_to_datetime)')

    @classmethod
    def datetime_to_string(cls, dt):
        """
        Conversts datetime to string.

        Arguments:
            dt {datetime} -- Datetime object

        Returns:
            str -- String equivalent to the datetime
        """
        try:
            return datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            raise FSOTimeException(
                'Not a valid timestamp (datetime_to_string)')

    @classmethod
    def from_path(cls, path):
        """
        Creates a new instance of TimeMetadata using path.

        Arguments:
            path {path} -- path object instance

        Returns:
            TimeMetadata -- Returns a instance of TimeMetadata
        """
        #str_atime = Time.datetime_to_string(path.atime)
        str_ctime = Time.datetime_to_string(path.ctime)
        str_mtime = Time.datetime_to_string(path.mtime)

        return Time(str_ctime, str_mtime)


@attr.s(frozen=True)
class MetaType(ObjectBase):
    """
    FileType class. Holds file type.
    """
    mimetype = attr.ib(validator=instance_of(str))
    binary = attr.ib(validator=instance_of(bool))
    link = attr.ib(validator=instance_of(str))

    @classmethod
    def from_path(cls, path, resolve_link=False):
        """
        Creates a new instance of FileType using path.

        Arguments:
            path {path} -- path object instance

        Returns:
            FileType -- Returns a instance of FileType
        """
        link = ''

        if path.islink():
            mimetype = 'inode/symlink'

            if resolve_link:
                link = Object.from_path(path.readlinkabs())
            else:
                link = str(path.readlinkabs())

        elif path.isdir():
            mimetype = 'inode/directory'

        elif path.isfile():
            mimetype = magic.from_file(
                path.abspath(), mime=True)

            if not mimetype:
                mimetype = 'unidentified'

        binary = MetaType.is_binary(path)
        return MetaType(mimetype, binary, link)

    @classmethod
    def is_binary(cls, path):
        """
        Verfies if file is binary

        Arguments:
            path {path} -- path object instance

        Returns:
            bool -- Returns True if the file is binary.
                    False if is not.
        """
        if path.isdir() or path.islink():
            return False

        _text_characters = (
            b''.join(bytes((i,)) for i in range(32, 127)) +
            b'\n\r\t\f\b')

        block = path.open('rb').read(512)

        if str(b"\x00") in block:
                # Files with null bytes are binary
            return False
        elif not block:
            # An empty file is considered a valid text file
            return True

        # Use translate's 'deletechars' argument to efficiently remove all
        # occurrences of _text_characters from the block

        text_chr = str.maketrans(dict.fromkeys(_text_characters))
        nontext = block.translate(text_chr)
        return not float(len(nontext)) / len(block) <= 0.30

        # nontext = block.translate(None, _text_characters)
        # return not float(len(nontext)) / len(block) <= 0.30


def hash_converter(value):
    if isinstance(value, dict):
        return Hash(**value)
    return value


def type_converter(value):
    if isinstance(value, dict):
        return Type(**value)
    return value


def time_converter(value):
    if isinstance(value, dict):
        return Time(**value)
    return value


def metatype_converter(value):
    if isinstance(value, dict):
        return MetaType(**value)
    return value


@attr.s(frozen=True)
class Object(ObjectBase):
    """
    File class. File representation.
    """
    path = attr.ib(validator=instance_of(str))
    name = attr.ib(validator=instance_of(str))
    ext = attr.ib(validator=instance_of(str))
    hash = attr.ib(validator=instance_of(Hash), converter=hash_converter)
    size = attr.ib(validator=instance_of(int))
    type = attr.ib(validator=instance_of(Type), converter=type_converter)
    time = attr.ib(validator=instance_of(Time), converter=time_converter)
    owner = attr.ib(validator=instance_of(str))
    mode = attr.ib(validator=instance_of(str))
    meta = attr.ib(validator=instance_of(MetaType),
                   converter=metatype_converter)

    @classmethod
    def from_path(cls, path):
        """
        Creates a new instance of File using path.

        Arguments:
            path {path} -- path object instance

        Returns:
            File -- Returns a instance of File
        """
        return Object(path=path.abspath(),
                      name=path.basename(),
                      ext=path.ext,
                      hash=Hash.from_path(path),
                      size=path.getsize(),
                      type=Type.from_path(path),
                      time=Time.from_path(path),
                      owner=path.get_owner(),
                      mode=str(oct(path.stat().st_mode))[2:],
                      meta=MetaType.from_path(path))
