#!/usr/bin/env python3

"""Module that manages users using filters loggers"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter datum for user data management"""
    for data in fields:
        message = re.sub(r"{}=(.*?)(?={})".format(data, separator),
                         data + "=" + redaction, message)
    return message
