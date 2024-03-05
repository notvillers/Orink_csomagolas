'''slave functions/definitions'''
from datetime import datetime

def get_time():
    '''return time in hh:mm:ss format'''
    return datetime.now().strftime('%H:%M:%S')

def reverse_list(list_to_reverse: list):
    '''reversing list'''
    return list_to_reverse[::-1]