'''slave functions/definitions'''
from datetime import datetime

def get_time():
    '''return time in hh:mm:ss format'''
    return datetime.now().strftime('%H:%M:%S')
