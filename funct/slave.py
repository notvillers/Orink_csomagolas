'''slave functions/definitions'''

from datetime import datetime
import platform
import random
import string
from time import sleep
from ping3 import ping

IS_WINDOWS = platform.system() == "Windows"

def get_time():
    '''returns time in hh:mm format'''
    return datetime.now().strftime('%H:%M')


def get_datetime():
    '''returns datetime in yyyy-mm-dd_hh-mm-ss format'''
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def reverse_list(list_to_reverse: list):
    '''reversing list'''
    return list_to_reverse[::-1]

def generate_random_string(length: int = 32):
    '''generates a random uppercase string of given length'''

    characters = string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_string_list(length: int = 100, string_length: int = 32):
    '''generates a list of unique random strings of given length'''

    random_strings = []
    while len(random_strings) < length:
        random_string = generate_random_string(string_length)
        if random_string not in random_strings:
            random_strings.append(random_string)
    return random_strings

def ping_srvr(server, retry_attempt: int = 0):
        '''pings with retry'''

        if retry_attempt != 0:
            response_time = ping(server)
            if response_time:
                return True
            else:
                sleep(5)
                ping_srvr(server, retry_attempt - 1)
        return False
