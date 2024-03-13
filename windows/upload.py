'''Upload'''

import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.json_handle
import funct.ftp_handle
import funct.file_handle
from funct.log import text_to_log

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS \ FELTÖLTÉS"
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE
BG_C = windows.gui_theme.BG_C
TXT_C = windows.gui_theme.TXT_C
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

# Popup
def sgpop(text):
    '''Drops a popup'''
    sg.popup_no_buttons(text, font = SMALL_F, title = HEADER)


# Main
def main():
    '''Main definition, runs the GUI'''

    text_to_log(HEADER + " started")

    header_layout = [
        [sg.Push(), sg.Text(HEADER, font = MEDIUM_BOLD), sg.Push()]
    ]

    text_layout = [
        [sg.Push(), sg.Text("Indulhat az adatok feltöltése?", font = MEDIUM_F), sg.Push()]
    ]

    options_layout = [
        [
            sg.Push(), sg.Button("IGEN", k = "-UPLOAD_YES-", font = SMALL_F, button_color = "green"),
            sg.Push(), sg.Button("NEM", k = "-UPLOAD_NO-", font = SMALL_F, button_color = "red"), sg.Push()
        ]
    ]

    info_layout = [
        [sg.Push(), sg.Text("", k = "-info-", font = SMALL_BOLD, text_color = "red"), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(HOSTNAME, font = FOOTER_F), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("", text_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("OPCIÓK", options_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("", info_layout, font = SMALL_BOLD, expand_x = True)],
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
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-" or event == "-UPLOAD_NO-":
            window.close()
            text_to_log(HEADER + " closed")
            return False
        # Uploads to ftp by ftp.json
        if event == "-UPLOAD_YES-":
            ftp_json = funct.json_handle.ftp_read()
            ftp_client = funct.ftp_handle.Client(
                hostname = ftp_json["hostname"],
                username = ftp_json["username"],
                password = ftp_json["password"]
            )
            if ftp_client.upload(config_path.db_path, ftp_json["directory"], config_path.db_name):
                sgpop("Sikeres feltöltés!")
                #funct.file_handle.clean_dir(os.path.join(config_path.path, config_path.db_subpath))
                window.close()
                text_to_log(HEADER + " closed")
                return True

    window.close()
    return False
