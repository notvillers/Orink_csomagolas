'''Main'''

import os
import PySimpleGUI as sg
import windows.gui_theme
from funct.log import text_to_log
from funct.slave import get_time, get_datetime
import config_path
import funct.json_handle
import funct.file_handle
from funct.sqlite_handle import Connection as sqlite_connection
from funct.db_config import CSOMAG_TABLE_CREATE, CSOMAG_TABLE_SELECT, CSOMAG_TABLE_INSERT, CSOMAG_TABLE_DELETE, CSOMAG_TABLE_UPDATE_BY_ID
from windows.edit import main as edit_main
from windows.settings import main as settings_main
from windows.upload import main as upload_main
from windows.admin import main as admin_main
from windows.event_viewer import main as event_main

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS"
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path
BSIZE = windows.gui_theme.BUTTON_SIZE
ISIZE = windows.gui_theme.INPUT_SIZE
B_GC = windows.gui_theme.BG_C
TXT_C = windows.gui_theme.TXT_C
OK_C = windows.gui_theme.OK_COLOR
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
BP_INTERVAL_S = config_path.BP_INTERVAL_S

# Variable(s)
exit_try_without_admin = 0

# Popup
def sgpop(text: str):
    '''Drops a popup'''

    sg.popup_no_buttons(text, font = SMALL_F, title = HEADER, keep_on_top = True)


def sgpop_yn(text: str = "Biztos?", color: str = "red"):
    '''Drops a yes or no popup
    returns True if Yes'''

    if sg.popup_yes_no(text, font = SMALL_F, keep_on_top = True, no_titlebar = True, background_color = color) == "Yes":
        return True
    return False


def backup_db():
    '''Backups the db to temp path'''

    datetime_string = get_datetime()
    backup_db_name = datetime_string + "_" + config_path.db_name
    backup_db_path = os.path.join(config_path.temp_path, backup_db_name)
    funct.file_handle.copy(config_path.db_path, backup_db_path)
    text_to_log(backup_db_path + " saved")


def place(elem):
    '''places element'''

    return sg.Column([[elem]], pad = (0, 0))


def main():
    '''Main definition, runs the GUI'''

    text_to_log(HEADER + " started")

    if funct.json_handle.create_config():
        sgpop("Kérlek töltsd ki a felhasználó adatokat!")
    if funct.json_handle.create_ftp():
        sgpop("Kérlek töltsd ki az FTP adatokat!")
    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]
    hostname = config_path.hostname

    local_db = sqlite_connection()
    local_db.execute(CSOMAG_TABLE_CREATE)
    columns, results = local_db.select(CSOMAG_TABLE_SELECT)

    backup_countdown = BP_INTERVAL_S

    header_layout = [
        [sg.Push(), sg.Text(HEADER, k = "-header-", font = MEDIUM_BOLD), sg.Push()]
    ]

    option_layout = [
        [
            sg.Input("", k = "-new_package-", font = SMALL_F),
            sg.Button("HOZZÁADÁS", k = "-ADD-", font = SMALL_F, bind_return_key = True, button_color = "green"),
            sg.Button("MÓDOSÍTÁS", k = "-EDIT-", font = SMALL_F),
            sg.Button("TÖRLÉS", k = "-DELETE-", font = SMALL_F, button_color = "red"),
            sg.Push(), sg.Text("", k = "-info-", font = MEDIUM_BOLD, text_color = "red"), sg.Push(),
            place(sg.Button("TEMP MENT", k = "-QUICK_BACKUP-", font = SMALL_F, button_color = "green", visible = False)),
            place(sg.Button("TEMP TÖRÖL", k = "-DELETE_BACKUP-", font = SMALL_F, button_color = "red", visible = False))
        ]
    ]

    packages_layout = [
        [
            sg.Table(
                values = results, 
                headings = columns,
                key = "-packages-",
                font = SMALL_F,
                justification = 'right',
                auto_size_columns = True,
                enable_events = True,
                enable_click_events = True,
                expand_x = True,
                expand_y = True,
                header_text_color = B_GC,
                header_background_color = TXT_C,
                sbar_background_color = TXT_C,
                sbar_frame_color = B_GC,
                sbar_trough_color = B_GC,
                vertical_scroll_only = False,
                alternating_row_color = OK_C,
            )
        ]
    ]

    settings_layout = [
        [
            sg.Push(), sg.Button("ADATOK", k = "-SETTINGS-", font = SMALL_F),
            sg.Push(), sg.Button("FELTÖLTÉS", k = "-UPLOAD-", font = SMALL_F), sg.Push(),
        ]
    ]

    footer_layout = [
        [sg.Text(HOSTNAME, k = "-hostname-", font = FOOTER_F), sg.Push(), sg.Text(get_time(), k = "-time-", font = FOOTER_F)]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True, k = "-header_frame-")],
        [sg.Frame("RÖGZÍTÉS", option_layout, font = SMALL_BOLD, expand_x = True, k = "-option_frame-")],
        [sg.Frame("CSOMAGOK", packages_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-packages_frame-")],
        [sg.Frame("BEÁLLÍTÁSOK", settings_layout, font = SMALL_BOLD, expand_x = True, k = "-settings_frame-")],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True, k = "-footer_frame-")]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = SGSIZE, icon = ICON_PATH)
    # 'esc' event
    window.bind("<Escape>", "-ESCAPE-")
    # 'ctrl' event
    window.bind("<Control-Key>", "-ctrl-")
    # 'ctrl+s' event
    window.bind("<Control-s>", "-ctrl_s-")
    window.bind("<Control-S>", "-ctrl_s-")
    # 'ctrl+a' event
    window.bind("<Control-a>", "-ctrl_a-")
    window.bind("<Control-A>", "-ctrl_a-")
    # 'ctrl+f' event
    window.bind("<Control-f>", "-ctrl_f-")
    window.bind("<Control-F>", "-ctrl_f-")
    # 'ctrl+e' event
    window.bind("<Control-e>", "-ctrl_e-")
    window.bind("<Control-E>", "-ctrl_e-")
    # 'ctrl+r' event
    window.bind("<Control-r>", "-ctrl_r-")
    window.bind("<Control-R>", "-ctrl_r-")

    window.Maximize()

    ctrl_event = False
    selected_item_id = False
    admin_mode = False

    while True:
        event, value = window.read(timeout = 1000)
        print("event: ", end = "\t"); print(event)
        print("value: ", end = "\t"); print(value)

        # ctrl event
        if event == "-ctrl-":
            if not ctrl_event:
                window["-SETTINGS-"].update("CTRL + A")
                window["-UPLOAD-"].update("CTRL + F")
                ctrl_event = not ctrl_event
                if admin_mode:
                    window["-hostname-"].update("KIKAPCSOLÁSA: CTRL+S | ESEMÉNY NAPLÓ: CTRL+E")
            else:
                window["-SETTINGS-"].update("ADATOK")
                window["-UPLOAD-"].update("FELTÖLTÉS")
                if admin_mode:
                    window["-hostname-"].update("RENDSZERGAZDA MÓD")
                ctrl_event = not ctrl_event

        # Toggle admin mode
        if event == "-ctrl_s-":
            text_to_log("-ctrl_s-")
            if not admin_mode:
                admin_mode = admin_main()
                if admin_mode:
                    text_to_log("ADMIN MODE ENABLED")
                    window["-QUICK_BACKUP-"].update(visible = True)
                    window["-DELETE_BACKUP-"].update(visible = True)
                    if not ctrl_event:
                        window["-hostname-"].update("RENDSZERGAZDA MÓD", background_color = "red", font = SMALL_BOLD)
                    else:
                        window["-hostname-"].update("KIKAPCSOLÁSA: CTRL+S | ESEMÉNY NAPLÓ: CTRL+E", background_color = "red", font = SMALL_BOLD)
            else:
                event = "-DISABLE_ADMIN-"

        # Disable admin mode
        if event == "-DISABLE_ADMIN-":
            text_to_log("-DISABLE_ADMIN-")
            admin_mode = False
            window["-QUICK_BACKUP-"].update(visible = False)
            window["-DELETE_BACKUP-"].update(visible = False)
            window["-hostname-"].update(HOSTNAME, background_color = B_GC, font = FOOTER_F)

        # Admin mode
        if event == "-QUICK_BACKUP-":
            text_to_log("-QUICK_BACKUP-")
            backup_db()
            window["-header-"].update("SIKERES MENTÉS", background_color = "green")
        if event == "-DELETE_BACKUP-":
            text_to_log("-DELETE_BACKUP-")
            funct.file_handle.clean_dir(config_path.temp_path)
            window["-header-"].update("MENTÉSEK TÖRÖLVE", background_color = "green")

        # Exit
        if event in ["Exit", "-ESCAPE-", sg.WIN_CLOSED]:
            global exit_try_without_admin
            if exit_try_without_admin > 4:
                sgpop("Nincs jogosultságod kilépni!")
                exit_try_without_admin = 0
            if admin_mode:
                text_to_log("EXIT")
                window.Close()
                return False
            if not admin_mode:
                exit_try_without_admin += 1
                text_to_log("TRYING TO EXIT WITHOUT ADMIN_MODE " + str(exit_try_without_admin))
            if event == sg.WIN_CLOSED:
                window.Close()
                return True

        # Restart
        if event == "-ctrl_r-" and admin_mode:
            return True

        # Timeout event
        if event == "__TIMEOUT__":
            window["-time-"].update(get_time())
            if backup_countdown > 0:
                backup_countdown -= 1
            else:
                if not admin_mode:
                    backup_db()
                    backup_countdown = BP_INTERVAL_S

        # Checking for table click
        if event is not None:
            if event[0] == "-packages-" and event[1] == "+CLICKED+" and event[2][0] not in (None, -1) and event[2][1] not in (None, -1):
                selected_item = results[event[2][0]]
                selected_item_id = selected_item[0]
                #print(selected_item)
                #print(selected_item_id)

        # Add
        if event == "-ADD-":
            if value["-new_package-"]:
                # If not repeatable package no.
                if not local_db.is_value_there(columns, results, "Csomagszám", value["-new_package-"]):
                    window["-info-"].update("")
                    local_db.insert(CSOMAG_TABLE_INSERT, (value["-new_package-"], usercode, hostname))
                    text_to_log("package no. " + value["-new_package-"] + " added")
                    columns, results = local_db.select(CSOMAG_TABLE_SELECT)
                    window["-new_package-"].update("")
                    window["-packages-"].update(values = results)
                else:
                    window["-info-"].update("Ismétlődés!")
                    window["-new_package-"].update("")
            else:
                window["-info-"].update("Üres csomagszám!")

        # Edit
        if event == "-EDIT-":
            if selected_item_id:
                update_item = edit_main(selected_item)
                if update_item is not None:
                    if not local_db.is_value_there(columns, results, "Csomagszám", update_item[1]):
                        window["-info-"].update("")
                        update_val = (update_item[1], update_item[0])
                        local_db.insert(CSOMAG_TABLE_UPDATE_BY_ID, (update_val))
                        text_to_log("UPDATE: " + str(update_item[0]) + " - " + str(update_item[1]))
                        columns, results = local_db.select(CSOMAG_TABLE_SELECT)
                        window["-packages-"].update(values = results)
                    else:
                        window["-info-"].update("Ismétlődés!")

        # Delete
        if event == "-DELETE-" and selected_item_id:
            if sgpop_yn("Biztosan törli?"):
                local_db.execute(CSOMAG_TABLE_DELETE, (selected_item_id))
                columns, results = local_db.select(CSOMAG_TABLE_SELECT)
                text_to_log("ID: " + str(selected_item_id) + " DELETED")
                window["-packages-"].update(values = results)

        # Settings
        if event in ["-SETTINGS-", "-ctrl_a-"]:
            text_to_log("-SETTINGS-")
            settings_main(admin_mode)
            config_json = funct.json_handle.config_read()
            usercode = config_json["usercode"]

        # Upload
        if event in ["-UPLOAD-", "-ctrl_f-"]:
            text_to_log("-UPLOAD-")
            succ_upload = upload_main()
            if succ_upload:
                if sgpop_yn("Törli a helyi adatokat?"):
                    text_to_log("DB DELETE")
                    window.close()
                    local_db.close()
                    funct.file_handle.clean_dir(os.path.join(config_path.path, config_path.DB_SUBPATH))
                    return True
                
        # Event viewer
        if event == "-ctrl_e-" and admin_mode:
            event_main()

    window.close()
    return False


if __name__ == "__main__":
    main_open = True
    while main_open:
        main_open = main()
