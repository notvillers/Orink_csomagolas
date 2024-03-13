'''Edits choosen package'''

import PySimpleGUI as sg
import windows.gui_theme
import config_path
from funct.log import text_to_log
from windows.popup import pop_esc_yn

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS \ MÓDOSÍTÁS"
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
HOSTNAME = config_path.hostname

# Main
def main(selected_item):
    '''Main definition, runs the GUI'''

    text_to_log(HEADER + " started")

    package_id = selected_item[0]
    package_no = selected_item[1]
    package_user = selected_item[2]

    header_layout = [
        [sg.Push(), sg.Text(HEADER, font = MEDIUM_BOLD), sg.Push()]
    ]

    package_layout = [
        [sg.Text("ID: ", font = SMALL_F), sg.Push(), sg.Input(package_id, font = SMALL_F, size = ISIZE, readonly = True, disabled_readonly_background_color = B_GC)],
        [sg.Text("Csomagszám: ", font = SMALL_F), sg.Push(), sg.Input(package_no, k = "-package_no-", font = SMALL_F, size = ISIZE)],
        [sg.Text("Rögzítő: ", font = SMALL_F), sg.Push(), sg.Input(package_user, font = SMALL_F, size = ISIZE, readonly = True, disabled_readonly_background_color = B_GC)]
    ]

    button_layout = [
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = SMALL_F, size = BSIZE, bind_return_key = True), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(HOSTNAME, font = FOOTER_F), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("CSOMAG", package_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("OPCIÓK", button_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True)]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = SGSIZE, icon = ICON_PATH, location = (0, 0))
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        event, value = window.read()
        #print("event: ", end = "\t"); print(event)
        #print("value: ", end = "\t"); print(value)
        # Exit
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            window.close()
            text_to_log(HEADER + " closed")
            return None
        # Update
        if event == "-UPDATE-":
            if value["-package_no-"]:
                window.close()
                text_to_log(HEADER + " closed")
                text_to_log("UPDATE")
                return [package_id, value["-package_no-"], package_user]
            pop_esc_yn(text = "Üres csomagszám nem rögzítehető!")

    window.close()
