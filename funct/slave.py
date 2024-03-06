'''slave functions/definitions'''
from datetime import datetime

def get_time():
    '''returns time in hh:mm:ss format'''
    return datetime.now().strftime('%H:%M:%S')


def get_datetime():
    '''returns datetime in yyyy-mm-dd_hh-mm-ss format'''
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def reverse_list(list_to_reverse: list):
    '''reversing list'''
    return list_to_reverse[::-1]