import re
import hashlib
import attr

from attr.validators import instance_of

from .object_base import ObjectBase
from .exceptions import FSOHashException


@attr.s(frozen=True)
class Hash(ObjectBase):
    """
    FileHash class. Used to hold file hashes.
    """
    sha512 = attr.ib(validator=instance_of(str))

    @sha512.validator
    def _validate_sha512(self, attribute, value):
        """
        Validates the sha512 field is valid using regex.

        Arguments:
            attribute {str} -- field name
            value {str} -- field value

        Returns:
            bool -- returns True if all sha512 is valid.
        """
        try:
            return re.match(r'^\w{128}$', value).group(0)
        except AttributeError:
            raise FSOHashException("Not a valid SHA512 hash")

    @classmethod
    def from_path(cls, path):
        """
        Creates a new instance of FileHash using path.

        Arguments:
            path {path} -- path object instance

        Returns:
            FileHash -- Returns a instance of FileHash
        """

        if path.isdir():
            hash_sha512 = hashlib.sha512()

            for file_ref in path.files():
                with open(file_ref, "rb") as file_ref:
                    for chunk in iter(lambda: file_ref.read(4096), b""):
                        hash_sha512.update(chunk)

            hash_str = hash_sha512.hexdigest()

        elif path.isfile():
            hash_str = path.read_hexhash('sha512')
        else:
            raise FSOHashException("FileSystem object not recognized")

        return Hash(hash_str)
