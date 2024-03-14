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

# Variables
IS_LINUX = config_path.IS_LINUX

def pop_esc_yn(header: str = "Figyelmeztetés!", text: str = "Biztos?", buttons: list = []):
    '''pops a popup which closes on <Escape> event'''

    text_to_log("pop_esc_yn: " + header + " started")
    
    text_layout = [
        [sg.Push(), sg.Text(text, font = SMALL_F), sg.Push()]
    ]

    events = ["-" + button + "-" for button in buttons]
    button_layout = [
        [sg.Button(button, k = "-" + button + "-", font = SMALL_F) for button in buttons]
    ]

    layout = [
        [sg.Frame("", text_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-text_frame-")],
    ]

    if buttons:
        layout.append([sg.Frame("", button_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-button_frame-")])

    window = sg.Window(header, layout, resizable = True, finalize = True, icon = ICON_PATH, keep_on_top = True)
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read(timeout = 15000)
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-", "__TIMEOUT__"]:
            window.close()
            text_to_log("pop_esc_yn: " + header + " closed")
            return None
        if event in events:
            window.close()
            text_to_log("pop_esc_yn: " + header + " closed")
            return event


def pop_esc_input(header: str = "Bevitel", text: str = "Bevitel", is_password: bool = False):
    '''pops an input popup which closes on <Escape> event'''

    text_to_log("pop_esc_input: " + header + " started")

    text_layout = [
        [sg.Push(), sg.Text(text, font = SMALL_F), sg.Push()]
    ]

    if not is_password:
        input_layout = [
            [sg.Push(), sg.Input(input, k = "-input-", font = SMALL_F, expand_x = True), sg.Push()]
        ]
    else:
        input_layout = [
            [sg.Push(), sg.Input(input, k = "-input-", font = SMALL_F, expand_x = True, password_char = "*"), sg.Push()]
        ]

    button_layout = [
        [sg.Push(), sg.Button("OK", k = "-OK-", font = SMALL_F, size = BSIZE), sg.Push()]
    ]

    layout = [
        [sg.Frame("", text_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-text_frame-")],
        [sg.Frame("", input_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-input_frame-")],
        [sg.Frame("", button_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-button_frame-")]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, icon = ICON_PATH, keep_on_top = True)
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read(timeout = 15000)
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-", "__TIMEOUT__"]:
            window.close()
            text_to_log("pop_esc_input: " + header + " closed")
            return None
        if event == "-OK-":
            window.close()
            text_to_log("pop_esc_input: " + header + " closed")
            if value["-input-"]:
                return value["-input-"]
            return None
