import json
from datetime import datetime

from config import cipher_suite


def convert_datetime(datetime_str: str) -> datetime:
    try:
        try:
            date_format = "%a, %d %b %Y %H:%M:%S %z"
            return datetime.strptime(datetime_str, date_format)
        except ValueError:
            date_format = "%a, %d %b %Y %H:%M:%S %Z"
            return datetime.strptime(datetime_str, date_format)
    except ValueError:
        date_format = "%a, %d %b %Y %H:%M:%S %z (%Z)"
        return datetime.strptime(datetime_str, date_format)


def encrypt_and_save(json_data, filename):
    encrypted_data = cipher_suite.encrypt(json_data.encode())

    with open(filename, 'wb') as file:
        file.write(encrypted_data)


def read_and_decrypt(filename):
    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)
    json_data = json.loads(decrypted_data.decode())

    return json_data
