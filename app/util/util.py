"""
util.py - Utility functions

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os

VERSION = "0.0.1"


def failure_message(message: str, code: str) -> dict:
    """
    Return a dict that is a standard failure message.

    Args:
        code (str): Mnemonic that never changes for this message
        message (str): Human-readable message text explaining the failure
    Returns:
        (dict): A message template.
    """
    return {
        'success': False,
        'message': message,
        'code': code,
        'version': VERSION,
    }


def get_env(key: str, default=None) -> str:
    """
    Get a configuration variable. For now, we use environment
    variables. That could change.

    Args:
        key (str): The config value to look for.
        default: The default value to return if key is not found.
    Returns:
        (str): Value found or default.
    """
    return os.environ.get(key, default)


def get_env_bool(key: str, default: bool) -> bool:
    """
    Get a boolean environment variable value, which might
    be represented as a string.

    Args:
        key (str): Environment variable to look for.
        default (bool): Default value
    Returns:
        (bool): The boolean value of the variable or the default
                if not found.
    """
    true_values = ['TRUE', 'T', 'Y', 'YES']

    value = os.environ.get(key, default)
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.upper() in true_values

    return value is True


def logmessage(message: str):
    """
    Log a message.

    Args:
        message (str): Message to log.
    Returns:
        None
    """
    print(message)


def success_message() -> dict:
    """
    Return a dict that is a standard failure message.

    Args:
        code (str): Mnemonic that never changes for this message
        message (str): Human-readable message text explaining the failure
    Returns:
        (dict): A message template.
    """
    return {
        'success': True,
        'message': "OK",
        'code': "OK",
        'version': VERSION,
    }
