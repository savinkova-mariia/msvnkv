from django.utils.text import slugify
from hashlib import md5
import os
import time
from unidecode import unidecode


def to_int(val, at_error=None):
    try:
        return int(val)
    except (ValueError, TypeError):
        return at_error


def transliterate(line):
    return slugify(unidecode(line))


def unique_upload_path(instance, filename):
    ext = os.path.splitext(filename)[-1]
    solt = str(time.time()) + filename
    filename = md5(solt.encode('utf8')).hexdigest() + ext
    basedir = os.path.join(instance._meta.app_label, instance._meta.model_name)

    return os.path.join(
        basedir,
        filename[:2],
        filename[2:4],
        filename[4:8],
        filename[8:16],
        filename[16:32],
        filename
    )
