#!/usr/bin/env python3

"""Module that manages users using filters loggers"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filter datum for user data management"""
    for data in fields:
        message = re.sub(r"{}=(.*?)(?={})".format(data, separator),
                         data + "=" + redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        """user format NotImplementedError"""
        record.msg: record.msg = filter_datum(self.fields, self.REDACTION,
                                              record.msg, self.SEPARATOR)
        return super().format(record)
