'''uuid gen'''

import uuid

def generate_uuid(length: int = 16):
    '''generate uuid'''
    return str(uuid.uuid4())[:length]
