# Settings

import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.json_handle
import funct.file_handle

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS \ ADATOK"
# Font
FOOTER_F = windows.gui_theme.FONT_ARIAL_FOOTER
FOOTER_BOLD = windows.gui_theme.FONT_ARIAL_FOOTER_BOLD
SMALL_F = windows.gui_theme.FONT_ARIAL_KICSI
SMALL_BOLD = windows.gui_theme.FONT_ARIAL_KICSI_BOLD
MEDIUM_F = windows.gui_theme.FONT_ARIAL_KOZEPES
MEDIUM_BOLD = windows.gui_theme.FONT_ARIAL_KOZEPES_BOLD
LARGE_F = windows.gui_theme.FONT_ARIAL_NAGY
LARGE_BOLD = windows.gui_theme.FONT_ARIAL_NAGY_BOLD
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE

# Popup
def sgpop(text: str):
    '''Drops a popup'''
    sg.popup_no_buttons(text, font = SMALL_F, title = HEADER)
    

# Main
def main():
    '''Main definition, runs the GUI'''

    users_list = funct.file_handle.csv_user_format(funct.file_handle.read_csv(config_path.users_path))

    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]

    header_layout = [
        [sg.Push(), sg.Text(HEADER, font = MEDIUM_BOLD), sg.Push()]
    ]

    setting_layout = [
        [sg.Text("Választott felhasználó azonosító:", font = SMALL_F)],
        [sg.Input(usercode, k = "-usercode-", font = SMALL_F, size = ISIZE, readonly = True, disabled_readonly_background_color = windows.gui_theme.BG_C)],
        [
            sg.Listbox(
                values = users_list,
                k = "-userlist-",
                font = SMALL_F,
                expand_y = True,
                enable_events = True,
                sbar_trough_color = windows.gui_theme.BG_C
            )
        ]
    ]

    option_layout = [
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = SMALL_F, size = BSIZE, bind_return_key = True), sg.Push()],
        [sg.Push(), sg.Button("TEMP TÖRLÉSE", k = "-TEMP_DEL-", font = SMALL_F, size = int(round(BSIZE * 1.3, 0)), button_color = "red"), sg.Push()]
    ]

    info_layout = [
        [sg.Push(), sg.Text("", k = "-info-", font = SMALL_BOLD, text_color = "red"), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.hostname, font = FOOTER_F), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("ADATOK", setting_layout, font = SMALL_BOLD, expand_x = True, expand_y = True)],
        [sg.Frame("OPCIÓK", option_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("", info_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True)]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path)
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        event, value = window.read()
        #print("event: ", end = "\t"); print(event)
        #print("value: ", end = "\t"); print(value)
        # Exit
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
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
            sgpop("Üres azonosító nem rögzíthető!")
        if event == "-TEMP_DEL-":
            funct.file_handle.clean_dir(config_path.temp_path)
            window["-info-"].update("./TEMP törölve/")

    window.close()
