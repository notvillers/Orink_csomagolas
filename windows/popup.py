'''Popup(s)'''

import PySimpleGUI as sg
import windows.gui_theme
import config_path
from funct.log import text_to_log

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE
B_GC = windows.gui_theme.BG_C
# Font
FOOTER_F = windows.gui_theme.FONT_ARIAL_FOOTER
FOOTER_BOLD = windows.gui_theme.FONT_ARIAL_FOOTER_BOLD
SMALL_F = windows.gui_theme.FONT_ARIAL_KICSI
SMALL_BOLD = windows.gui_theme.FONT_ARIAL_KICSI_BOLD
MEDIUM_F = windows.gui_theme.FONT_ARIAL_KOZEPES
MEDIUM_BOLD = windows.gui_theme.FONT_ARIAL_KOZEPES_BOLD
LARGE_F = windows.gui_theme.FONT_ARIAL_NAGY
LARGE_BOLD = windows.gui_theme.FONT_ARIAL_NAGY_BOLD

def pop_esc_yn(header: str = "Figyelmeztetés!", text: str = "Biztos?", buttons: list = []):
    '''pops a popup which closes on <Escape> event'''

    text_to_log("pop: " + header + " started")
    
    text_layout = [
        [sg.Push(), sg.Text(text, font = SMALL_F), sg.Push()]
    ]

    events_for_buttons = ["-" + button + "-" for button in buttons]
    button_layout = [
        [sg.Button(button, k = "-" + button + "-", font = SMALL_F) for button in buttons]
    ]

    layout = [
        [sg.Frame("", text_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-text_frame-")],
        [sg.Frame("", button_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-button_frame-")]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, icon = ICON_PATH)
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            window.close()
            text_to_log("pop: " + header + " closed")
            return None
        if event in events_for_buttons:
            window.close()
            text_to_log("pop: " + header + " closed")
            return event
