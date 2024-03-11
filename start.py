'''starts main.main()'''

from main import main

if __name__ == "__main__":
    MAIN_OPEN = True
    IS_ADMIN = False
    while MAIN_OPEN:
        if not IS_ADMIN:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = False)
        else:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = True)
            
# TODO: logolásnál alábbi hiba windowson
    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc1 in position 44: invalid start byte
