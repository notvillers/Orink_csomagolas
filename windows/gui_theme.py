'''Configuration for the PySimpleGUI'''

import funct.resolution

# Font
FONT = 'Arial'
FONT_ARIAL_FOOTER = (FONT, 10)
FONT_ARIAL_KICSI = (FONT, 15)
FONT_ARIAL_KOZEPES = (FONT, 25)
FONT_ARIAL_NAGY = (FONT, 40)
# Bold
FONT_ARIAL_FOOTER_BOLD = (FONT, 10, "bold")
FONT_ARIAL_KICSI_BOLD = (FONT, 15, "bold")
FONT_ARIAL_KOZEPES_BOLD = (FONT, 25, "bold")
FONT_ARIAL_NAGY_BOLD = (FONT, 40, "bold")

# Colors + Theme
BG_C = '#93B1C3'
OK_COLOR = '#B8DDF5'
ERR_COLOR = '#F8665D'
TXT_C = "black"
BTT_C = BG_C + " on " + TXT_C

o8_theme = {
    'BACKGROUND': BG_C,
    'TEXT': TXT_C,
    'INPUT': '#B8DDF5',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#c7e78b',
    'BUTTON': (BG_C, TXT_C),
    'PROGRESS': ('#01826B', '#D0D0D0'),
    'BORDER': 3,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

# Size
sc_width, sc_height = funct.resolution.get_primary()

SC_PERCENT = 1
sgsize = (
    int(round(sc_width * SC_PERCENT, 0)), 
    int(round(sc_height * SC_PERCENT, 0))
)

MAIN_PERCENT = 1
main_sgisze = ( 
    int(round(sgsize[0] * MAIN_PERCENT, 0)),
    int(round(sgsize[1] * MAIN_PERCENT, 0))
)

# Button size
BUTTON_SIZE = 12

# Input size
INPUT_SIZE = 30
