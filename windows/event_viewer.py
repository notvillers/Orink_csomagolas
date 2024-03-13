'''Event viewer'''

import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.log
import funct.file_handle
import funct.slave

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "ESEMÉNYNAPLÓ"
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE
BG_C = "red"
# Font
FOOTER_F = windows.gui_theme.FONT_ARIAL_FOOTER
FOOTER_BOLD = windows.gui_theme.FONT_ARIAL_FOOTER_BOLD
SMALL_F = windows.gui_theme.FONT_ARIAL_KICSI
SMALL_BOLD = windows.gui_theme.FONT_ARIAL_KICSI_BOLD
MEDIUM_F = windows.gui_theme.FONT_ARIAL_KOZEPES
MEDIUM_BOLD = windows.gui_theme.FONT_ARIAL_KOZEPES_BOLD
LARGE_F = windows.gui_theme.FONT_ARIAL_NAGY
LARGE_BOLD = windows.gui_theme.FONT_ARIAL_NAGY_BOLD

def main():
    '''Main definition, runs the GUI'''

    log = funct.file_handle.read_file_content(funct.log.LOG_PATH)

    event_layout = [
        [
            sg.Multiline(
                log, 
                k = "-multiline_log-",
                font = SMALL_BOLD,
                expand_x = True,
                expand_y = True,
                justification = "left",
                background_color = "white",
                sbar_background_color = BG_C,
                sbar_frame_color = BG_C,
                sbar_trough_color = BG_C,
                sbar_arrow_color = "black"
            )
        ],
        [sg.Push(background_color = BG_C), sg.Text("CTRL+E = " + HEADER, font = SMALL_F, background_color = BG_C), sg.Push(background_color = BG_C)]
    ]

    layout = [
        [sg.Frame(HEADER, event_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, background_color = BG_C)]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = SGSIZE, icon = ICON_PATH, background_color = "red", location = (0, 0))
    # 'esc' event
    window.bind("<Escape>", "-ESCAPE-")
    
    window.Maximize()

    while True:
        event, values = window.read()

        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            window.Close()
            funct.log.text_to_log(HEADER + " closed")
            break

    window.Close()