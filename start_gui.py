#!/usr/bin/env python3
'''starts main.main()'''

from start import main

if __name__ == "__main__":
    MAIN_OPEN = True
    IS_ADMIN = False
    while MAIN_OPEN:
        if not IS_ADMIN:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = False)
        else:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = True)
