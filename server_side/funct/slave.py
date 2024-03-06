'''slave for minimal tasks'''

from datetime import datetime

def current_datetime_to_string():
    '''returns current datetime in yyyy-mm-dd_hh-mm-ss format'''

    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
