import json
import logging
import os
import re
import uuid
from io import BytesIO
from typing import Any, Dict, Generator, List, Optional

import redis
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists

_logger = logging.getLogger(__name__)

_valid_email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

_minio_client = Minio(endpoint=os.environ['MINIO_URL'],
                      access_key=os.environ['MINIO_ACCESS_KEY'],
                      secret_key=os.environ['MINIO_SECRET_KEY'],
                      secure=False)

_redis_client = redis.Redis(host=os.environ['REDIS_URL'],
                            port=int(os.environ['REDIS_PORT']),
                            db=int(os.environ['REDIS_DB']))


def add_entry(entry: Dict) -> bool:
    """Add entry

    :param entry: dictionary with the following keys ['description', 'file']
    :return: boolean success flag
    """

    file_content = entry['file']['body']
    file_filename = str(uuid.uuid4())

    try:
        _minio_client.make_bucket("entries")
    except (BucketAlreadyOwnedByYou, BucketAlreadyExists):
        pass
    except ResponseError:
        _logger.exception('Minio response error.')
        return False

    try:
        _minio_client.put_object('entries', file_filename, BytesIO(file_content), len(file_content), 'text/plain')
    except ResponseError:
        _logger.exception('Minio - saving the file failed.')
        return False

    entry['file'] = file_filename

    try:
        _redis_client.set(file_filename, json.dumps(entry))
    except:
        _logger.exception('Setting a redis key failed.')
        return False

    return True


def validate_entries(entry: Dict) -> List[str]:
    """Validate entry

    :param entry: dictionary with the following keys ['description', 'file']
    :return: list of errors
    """
    errors = []

    # Maybe it would be wiser to have some minimal required amount of characters.
    if len(entry['description'].strip()) == 0:
        errors.append('Your description is empty. Please provide a description.')

    if entry['file'] is None:
        errors.append('You did not attach a file. Please attach your file.')

    return errors


def get_entries() -> List[Dict]:
    """Returns entries

    :return: list of dictionaries with the following keys ['description', 'file']
    """
    return [json.loads(_redis_client.get(item)) for item in _redis_client.scan_iter()]


def get_file_stream(name: str) -> Generator[Optional[bytes], Any, None]:
    """Get the correct file from minio.

    :param name: name (UUID) of the requested file
    :return: requested file as iterable stream of bytes
    """
    return _minio_client.get_object('entries', name).stream()
