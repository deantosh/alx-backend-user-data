#!/usr/bin/env python3
"""
1. Task 0:

Write a function called filter_datum that returns the log message obfuscated:

Arguments:
 - fields: a list of strings representing all fields to obfuscate
 - redaction: a string representing by what the field will be obfuscated
 - message: a string representing the log line
 - separator: a string representing by which character is separating all
   fields in the log line (message)
The function should use a regex to replace occurrences of certain field values.
filter_datum should be less than 5 lines long and use re.sub to perform the
substitution with a single re

1. Task 1:

Update the class to accept a list of strings fields constructor argument.
Implement the format method to filter values in incoming log records using
filter_datum. Values for fields in fields should be filtered.
DO NOT extrapolate FORMAT manually. The format method should be less than 5
lines long.
"""
import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns an obfuscated log message
    """
    obs_message = message
    for field in fields:
        pattern = r"{field}=.*?{separator}".format(field=field,
                                                   separator=separator)
        obs_message = re.sub(pattern, f"{field}={redaction}{separator}",
                             obs_message)
    return obs_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
