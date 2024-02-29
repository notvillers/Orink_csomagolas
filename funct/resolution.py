# Resolution handler

from screeninfo import get_monitors

# Return the resolution of primary display
def get_primary():
	for disp in get_monitors():
		if len(get_monitors()) > 1:
			if disp.is_primary == True:
				return disp.width, disp.height
		return disp.width, disp.height
