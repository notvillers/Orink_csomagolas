from screeninfo import get_monitors

# Elsődleges monitor felbontását adja vissza
def get_primary():
    for disp in get_monitors():
        if disp.is_primary == True:
            return disp.width, disp.height