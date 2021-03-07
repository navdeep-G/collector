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


def add_feedback(feedback: Dict) -> bool:
    """Add feedback consisting of email, feedback (actual text), rating, and attached log file.

    :param feedback: dictionary with the following keys ['email', 'feedback', 'rating', 'log']
    :return: boolean success flag
    """

    log_content = feedback['log']['body']
    log_filename = str(uuid.uuid4())

    try:
        _minio_client.make_bucket("logs")
    except (BucketAlreadyOwnedByYou, BucketAlreadyExists):
        pass
    except ResponseError:
        _logger.exception('Minio response error.')
        return False

    try:
        _minio_client.put_object('logs', log_filename, BytesIO(log_content), len(log_content), 'text/plain')
    except ResponseError:
        _logger.exception('Minio - saving the log failed.')
        return False

    feedback['log'] = log_filename

    try:
        _redis_client.set(log_filename, json.dumps(feedback))
    except:
        _logger.exception('Setting a redis key failed.')
        return False

    return True


def validate_feedback(feedback: Dict) -> List[str]:
    """Validate feedback consisting of email, feedback (actual text), rating, and attached log file.

    :param feedback: dictionary with the following keys ['email', 'feedback', 'rating', 'log']
    :return: list of errors
    """
    errors = []

    if not _valid_email_regex.match(feedback['email']):
        errors.append('Email is not correct. Please provide correct email address.')

    # Maybe it would be wiser to have some minimal required amount of characters.
    if len(feedback['feedback'].strip()) == 0:
        errors.append('Your feedback is empty. Please provide your feedback.')

    # Should not happen, since the rating is preselected to 3 and it should not be possible for accidentally uncheck
    # radio button so that it leaves whole radio button group unchecked but better safe than sorry...
    if feedback['rating'] is None:
        errors.append('Please provide rating.')

    if feedback['log'] is None:
        errors.append('You did not attach log file. Please attach your log file.')

    return errors


def get_feedbacks() -> List[Dict]:
    """Returns feedbacks

    :return: list of dictionaries with the following keys ['email', 'feedback', 'rating', 'log']
    """
    return [json.loads(_redis_client.get(item)) for item in _redis_client.scan_iter()]


def get_log_stream(name: str) -> Generator[Optional[bytes], Any, None]:
    """Get the correct log from minio.

    :param name: name (UUID) of the requested log
    :return: requested log as iterable stream of bytes
    """
    return _minio_client.get_object('logs', name).stream()
