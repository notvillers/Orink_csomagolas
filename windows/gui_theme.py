# Configuration for the PySimpleGUI

# Font
font = 'Arial'
font_arial_footer = (font, 10)
font_arial_kicsi = (font, 15)
font_arial_kozepes = (font, 25)
font_arial_nagy = (font, 40)
# Bold
font_arial_footer_bold = (font, 10, "bold")
font_arial_kicsi_bold = (font, 15, "bold")
font_arial_kozepes_bold = (font, 25, "bold")
font_arial_nagy_bold = (font, 40, "bold")

# Colors + Theme
bg_c = '#93B1C3'
ok_color = '#B8DDF5'
err_color = '#F8665D'
txt_c = "black"
btt_c = bg_c + " on " + txt_c

o8_theme = {
    'BACKGROUND': bg_c,
    'TEXT': txt_c,
    'INPUT': '#B8DDF5',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#c7e78b',
    'BUTTON': (bg_c, txt_c),
    'PROGRESS': ('#01826B', '#D0D0D0'),
    'BORDER': 3,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}

# Size
import funct.resolution
sc_width, sc_height = funct.resolution.get_primary()
sc_percent = 0.85
sgsize = (
    int(round(sc_width * sc_percent, 0)), 
    int(round(sc_height * sc_percent, 0))
)

main_percent = 0.3
main_sgisze = ( 
    int(round(sgsize[0] * main_percent, 0)),
    int(round(sgsize[1] * main_percent, 0))
)

# Button size
button_size = 12

# Input size
input_size = 30