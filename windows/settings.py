# Settings

import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.json_handle
import funct.file_handle
from funct.log import text_to_log, delete_log

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

def place(elem):
    '''places element'''

    return sg.Column([[elem]], pad = (0, 0))

# Main
def main(admin_mode):
    '''Main definition, runs the GUI'''

    ftp_info = "Rendszergazda szükséges" if not admin_mode else ""
    ftp = funct.json_handle.ftp_read()

    users_list = funct.file_handle.csv_user_format(funct.file_handle.read_csv(config_path.users_path))

    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]

    header_layout = [
        [sg.Push(), sg.Text(HEADER, k = "-header-", font = MEDIUM_BOLD), sg.Push()]
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
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = SMALL_F, size = BSIZE, bind_return_key = True), sg.Push()]
    ]

    ftp_layout = [
        [sg.Push(), sg.Text(ftp_info, k = "-info-", font = SMALL_BOLD, text_color = "red"), sg.Push()],
        [
            place(sg.Input(ftp["hostname"], k = "-ftp_hostname-", font = SMALL_F , tooltip = "ftp hostname", visible = False)),
            place(sg.Input(ftp["username"], k = "-ftp_username-", font = SMALL_F, tooltip = "ftp username", visible = False))
        ],
        [
            place(sg.Input(ftp["password"], k = "-ftp_password-", font = SMALL_F, tooltip = "ftp password", visible = False)),
            place(sg.Input(ftp["directory"], k = "-ftp_directory-", font = SMALL_F, tooltip = "ftp directory", visible = False))
        ],
        [
            place(sg.Button("FRISSÍTÉS", k = "-FTP_UPDATE-", font = SMALL_F, size = int(round(BSIZE * 1.3, 0)), button_color = "red", visible = False)),
            place(sg.Text("", k = "-ftp_info-", font = SMALL_BOLD, text_color = "red", visible = False))
        ]
    ]

    log_layout = [
        [
            place(sg.Button("LOG TÖRLÉSE", k = "-LOG_DELETE-", font = SMALL_F, size = int(round(BSIZE * 1.3, 0)), button_color = "red", visible = "False")),
            place(sg.Text("", k = "-log_info-", font = SMALL_BOLD, text_color = "red", visible = False))
        ]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.hostname, font = FOOTER_F), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("ADATOK", setting_layout, font = SMALL_BOLD, expand_x = True, expand_y = True)],
        [sg.Frame("OPCIÓK", option_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("FTP", ftp_layout, font = SMALL_BOLD, expand_x = True, visible = False, k = "-ftp_frame-")],
        [sg.Frame("LOG", log_layout, font= SMALL_BOLD, expand_x = True, visible = False, k = "-log_frame-")],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True)]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path)
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        if admin_mode:
            # ftp layout
            window["-header-"].update("RENDSZERGAZDA MÓD", background_color = "red")
            window["-ftp_frame-"].update(visible = True)
            window["-ftp_hostname-"].update(visible = True)
            window["-ftp_username-"].update(visible = True)
            window["-ftp_password-"].update(visible = True)
            window["-ftp_directory-"].update(visible = True)
            window["-FTP_UPDATE-"].update(visible = True)
            window["-ftp_info-"].update(visible = True)
            # log layout
            window["-log_frame-"].update(visible = True)
            window["-LOG_DELETE-"].update(visible = True)
            window["-log_info-"].update(visible = True)
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
        
        # FTP UPDATE
        if event == "-FTP_UPDATE-":
            hostname = (value["-ftp_hostname-"] if value["-ftp_hostname-"] != "" else None)
            username = (value["-ftp_username-"] if value["-ftp_username-"] != "" else None)
            password = (value["-ftp_password-"] if value["-ftp_password-"] != "" else None)
            directory = (value["-ftp_directory-"] if value["-ftp_directory-"] != "" else None)
            funct.json_handle.ftp_update(hostname = hostname, username = username, password = password, directory = directory)
            window["-ftp_info-"].update("frissítve")

        # LOG DELETE
        if event == "-LOG_DELETE-":
            delete_log()
            window["-log_info-"].update("törölve")

    window.close()
