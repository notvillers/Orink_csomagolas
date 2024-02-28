# Settings

import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.json_handle
import funct.file_handle

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - CSOMAGOLÁS \ ADATOK"
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

    users_list = funct.file_handle.csv_user_format(funct.file_handle.read_csv(config_path.users_path))

    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]

    header_layout = [
        [sg.Push(), sg.Text(header, font = medium_bold), sg.Push()]
    ]

    setting_layout = [
        [sg.Text("Felhasználó azonosító:", font = small_f), sg.Push(), sg.Input(usercode, k = "-usercode-", font = small_f, size = isize)],
        [sg.Push(), sg.Push(), sg.Push(), sg.Listbox(values = users_list, k = "-userlist-", font = small_f, expand_x = True, expand_y = True, enable_events = True, sbar_trough_color = windows.gui_theme.bg_c)]
    ]

    option_layout = [
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = small_f, size = bsize, bind_return_key = True), sg.Push()],
        [sg.Push(), sg.Button("TEMP TÖRLÉSE", k = "-TEMP_DEL-", font = small_f, size = int(round(bsize * 1.3, 0)), button_color = "red"), sg.Push()]
    ]

    info_layout = [
        [sg.Push(), sg.Text("", k = "-info-", font = small_bold, text_color = "red"), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.hostname, font = footer_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_bold, expand_x = True)],
        [sg.Frame("ADATOK", setting_layout, font = small_bold, expand_x = True, expand_y = True)],
        [sg.Frame("OPCIÓK", option_layout, font = small_bold, expand_x = True)],
        [sg.Frame("", info_layout, font = small_bold, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = small_bold, expand_x = True)]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path)
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        event, value = window.read()
        print("event: ", end = "\t"); print(event)
        print("value: ", end = "\t"); print(value)
        # Exit
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-":
            window.close()
            break
        # Update
        if event == "-userlist-":
            user = value["-userlist-"][0].split(" - ")[0]
            window["-usercode-"].update(user)
        if event == "-UPDATE-":
            if value["-usercode-"]:
                funct.json_handle.config_update(usercode = value["-usercode-"])
                window.close()
                break
            else:
                sgpop("Üres azonosító nem rögzíthető!")
        if event == "-TEMP_DEL-":
            funct.file_handle.clean_dir(config_path.temp_path)
            window["-info-"].update("./TEMP törölve/")

    window.close()