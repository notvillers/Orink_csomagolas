# Upload

import PySimpleGUI as sg
import os
import windows.gui_theme
import config_path
import funct.json_handle
import funct.ftp_handle
import funct.file_handle

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - CSOMAGOLÁS \ FELTÖLTÉS"
# Font
footer_bold = windows.gui_theme.font_arial_footer_bold
footer_f = windows.gui_theme.font_arial_footer
small_f = windows.gui_theme.font_arial_kicsi
small_bold = windows.gui_theme.font_arial_kicsi_bold
medium_f = windows.gui_theme.font_arial_kozepes
medium_bold = windows.gui_theme.font_arial_kozepes_bold
large_f = windows.gui_theme.font_arial_nagy
large_bold = windows.gui_theme.font_arial_nagy_bold
bsize = windows.gui_theme.button_size
isize = windows.gui_theme.input_size

# Popup
def sgpop(text):
    sg.popup_no_buttons(text, font = small_f, title = header)

# Main
def main():

    header_layout = [
        [sg.Push(), sg.Text(header, font = medium_bold), sg.Push()]
    ]

    text_layout = [
        [sg.Push(), sg.Text("Indulhat az adatok feltöltése?", font = medium_f), sg.Push()]
    ]

    options_layout = [
        [sg.Push(), sg.Button("IGEN", k = "-UPLOAD_YES-", font = small_f, button_color = "green", size = bsize), sg.Push(), sg.Button("NEM", k = "-UPLOAD_NO-", font = small_f, button_color = "red", size = bsize), sg.Push()]
    ]

    info_layout = [
        [sg.Push(), sg.Text("", k = "-info-", font = small_bold, text_color = "red"), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.hostname, font = footer_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_bold, expand_x = True)],
        [sg.Frame("", text_layout, font = small_bold, expand_x = True)],
        [sg.Frame("OPCIÓK", options_layout, font = small_bold, expand_x = True)],
        [sg.Frame("", info_layout, font = small_bold, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = small_bold, expand_x = True)]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path)
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        event, value = window.read()
        #print("event: ", end = "\t"); print(event)
        #print("value: ", end = "\t"); print(value)
        # Exit
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-" or event == "-UPLOAD_NO-":
            window.close()
            return False
        # Uploads to ftp by ftp.json
        if event == "-UPLOAD_YES-":
            ftp_json = funct.json_handle.ftp_read()
            ftp_client = funct.ftp_handle.Client(
                hostname = ftp_json["hostname"],
                username = ftp_json["username"],
                password = ftp_json["password"]
            )
            if ftp_client.upload(config_path.db_path, ftp_json["directory"], config_path.db_name) == True:
                sgpop("Sikeres feltöltés!")
                funct.file_handle.clean_dir(os.path.join(config_path.path, config_path.db_subpath))
                window.close()
                return True

    window.close()
    return False