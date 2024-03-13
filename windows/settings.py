'''Settings'''

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
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE
BG_C = windows.gui_theme.BG_C
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
def sgpop(text: str):
    '''Drops a popup'''
    sg.popup_no_buttons(text, font = SMALL_F, title = HEADER)

def place(elem):
    '''places element'''

    return sg.Column([[elem]], pad = (0, 0))

# Main
def main(admin_mode):
    '''Main definition, runs the GUI'''

    text_to_log(HEADER + " started")

    ftp = funct.json_handle.ftp_read()

    users_list = funct.file_handle.csv_user_format(funct.file_handle.read_csv(config_path.users_path))

    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]

    header_layout = [
        [sg.Push(), sg.Text(HEADER, k = "-header-", font = MEDIUM_BOLD), sg.Push()]
    ]

    setting_layout = [
        [sg.Text("Választott felhasználó azonosító:", font = SMALL_F)],
        [sg.Input(usercode, k = "-usercode-", font = SMALL_F, size = ISIZE, readonly = not admin_mode, disabled_readonly_background_color = BG_C)],
        [
            sg.Listbox(
                values = users_list,
                k = "-userlist-",
                font = SMALL_F,
                expand_y = True,
                enable_events = True,
                sbar_trough_color = BG_C
            )
        ],
        [sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = SMALL_F, bind_return_key = True)]
    ]

    ftp_layout = [
        [
            place(sg.Input(ftp["hostname"], k = "-ftp_hostname-", font = SMALL_F , tooltip = "ftp hostname", visible = False)),
            place(sg.Input(ftp["username"], k = "-ftp_username-", font = SMALL_F, tooltip = "ftp username", visible = False))
        ],
        [
            place(sg.Input(ftp["password"], k = "-ftp_password-", font = SMALL_F, tooltip = "ftp password", visible = False)),
            place(sg.Input(ftp["directory"], k = "-ftp_directory-", font = SMALL_F, tooltip = "ftp directory", visible = False))
        ],
        [
            place(sg.Button("FRISSÍTÉS", k = "-FTP_UPDATE-", font = SMALL_F, button_color = "red", visible = False)),
            place(sg.Text("", k = "-ftp_info-", font = SMALL_BOLD, text_color = "red", visible = False))
        ]
    ]

    log_layout = [
        [
            place(sg.Button("TISZTÍTÁS", k = "-LOG_DELETE-", font = SMALL_F, button_color = "red", visible = "False")),
            place(sg.Text("", k = "-log_info-", font = SMALL_BOLD, text_color = "red", visible = False))
        ]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(HOSTNAME, k = "-hostname-", font = FOOTER_F), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True)],
        [sg.Frame("ADATOK", setting_layout, font = SMALL_BOLD, expand_x = True, expand_y = True)],
        [sg.Frame("FTP - RENDSZERGAZDA MÓD", ftp_layout, font = SMALL_BOLD, expand_x = True, visible = False, k = "-ftp_frame-")],
        [sg.Frame("LOG - RENDSZERGAZDA MÓD", log_layout, font= SMALL_BOLD, expand_x = True, visible = False, k = "-log_frame-")],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True)]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = SGSIZE, icon = ICON_PATH, location = (0, 0))
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        if admin_mode:
            # ftp layout
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
            # footer
            window["-hostname-"].update("RENDSZERGAZDA MÓD", font = SMALL_BOLD, background_color = "red")
        event, value = window.read()
        #print("event: ", end = "\t"); print(event)
        #print("value: ", end = "\t"); print(value)
        # Exit
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            window.close()
            text_to_log(HEADER + " closed")
            break

        # Update
        if event == "-userlist-":
            user = value["-userlist-"][0].split(" - ")[0]
            window["-usercode-"].update(user)
        if event == "-UPDATE-":
            if value["-usercode-"]:
                funct.json_handle.config_update(usercode = value["-usercode-"])
                text_to_log("-UPDATE-")
                text_to_log(HEADER + " closed")
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
            text_to_log("-FTP_UPDATE-")
            window["-ftp_info-"].update("frissítve")

        # LOG DELETE
        if event == "-LOG_DELETE-":
            delete_log()
            text_to_log("-LOG_DELETE-")
            window["-log_info-"].update("törölve")

    window.close()
