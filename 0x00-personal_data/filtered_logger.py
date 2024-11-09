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

Task 2:

Implement a get_logger function that takes no arguments and returns a
logging.Logger object.
The logger should be named "user_data" and only log up to logging.INFO level.
It should not propagate messages to other loggers. It should have a
StreamHandler with RedactingFormatter as formatter.
Create a tuple PII_FIELDS constant at the root of the module containing the
fields from user_data.csv that are considered PII. PII_FIELDS can contain
only 5 fields - choose the right list of fields that can are considered as
“important” PIIs or information that you must hide in your logs. Use it to
parameterize the formatter.

4. Task 3:
Implement a get_db function that returns a connector to the database
(mysql.connector.connection.MySQLConnection object).
 - Use the os module to obtain credentials from the environment
 - Use the module mysql-connector-python to connect to the MySQL database
   (pip3 install mysql-connector-python)
"""
import re
import os
import logging
from typing import List
import mysql.connector
from mysql.connector import connection


# Define PII fields
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Filters a message and returns an obfuscated log message
    """
    obs_message = message

    for field in fields:
        pattern = r"({}=).*?(?={}|$)".format(
            re.escape(field), re.escape(separator)
        )
        obs_message = re.sub(pattern, r"\1" + redaction,
                             obs_message)
    return obs_message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter record msg attribute to redact specified fields. Add format
           on the log record based on the FORMATTER variable which defines
           the format of the output.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object
    """
    # Get and configure a logger object
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up streamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """Returns a connector to the database
    """
    # Get db credentials from environment variable
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    db_pass = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Connect to the database
    conn = mysql.connector.connect(
        user=db_user,
        password=db_pass,
        host=db_host,
        database=db_name
    )

    return conn


def main():
    """Retrieves all rows in the User table
    """
    # Get logger object with PII_FIELDS redaction
    logger = get_logger()

    # Get the connection object
    conn = get_db()
    cursor = conn.cursor()

    # Execute SQL queries
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Get row headers
    headers = [field[0] for field in cursor.description]
    # Format the rows
    for row in rows:
        # Create a log record from the row
        log_message = '; '.join(
            f"{field}={value}" for field, value in zip(headers, row))
        logger.info(log_message)

    # Close database connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
