# Main

import os
from datetime import datetime
import PySimpleGUI as sg
import windows.gui_theme
from funct.log import text_to_log
from funct.slave import get_time
import config_path
import funct.json_handle
import funct.file_handle
from funct.sqlite_handle import Connection as sqlite_connection
from funct.db_config import CSOMAG_TABLE_CREATE, CSOMAG_TABLE_SELECT, CSOMAG_TABLE_INSERT, CSOMAG_TABLE_DELETE, CSOMAG_TABLE_UPDATE_BY_ID
from windows.edit import main as edit_main
from windows.settings import main as settings_main
from windows.upload import main as upload_main
from windows.admin import main as admin_main

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS"
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
    datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_db_name = datetime_string + "_" + config_path.db_name
    backup_db_path = os.path.join(config_path.temp_path, backup_db_name)
    funct.file_handle.copy(config_path.db_path, backup_db_path)
    text_to_log(backup_db_path + " saved")


def place(elem):
    '''places element'''

    return sg.Column([[elem]], pad = (0, 0))

# Main
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

    backup_countdown = config_path.BP_INTERVAL_S

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
                header_text_color = windows.gui_theme.BG_C,
                header_background_color = windows.gui_theme.TXT_C,
                sbar_background_color = windows.gui_theme.TXT_C,
                sbar_frame_color = windows.gui_theme.BG_C,
                sbar_trough_color = windows.gui_theme.BG_C,
                vertical_scroll_only = False,
                alternating_row_color = windows.gui_theme.OK_COLOR,
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
        [sg.Text(config_path.hostname, k = "-hostname-", font = FOOTER_F), sg.Push(), sg.Text(get_time(), k = "-time-", font = FOOTER_F)]
    ]

    layout = [
        [sg.Frame("", header_layout, font = SMALL_BOLD, expand_x = True, k = "-header_frame-")],
        [sg.Frame("RÖGZÍTÉS", option_layout, font = SMALL_BOLD, expand_x = True, k = "-option_frame-")],
        [sg.Frame("CSOMAGOK", packages_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-packages_frame-")],
        [sg.Frame("BEÁLLÍTÁSOK", settings_layout, font = SMALL_BOLD, expand_x = True, k = "-settings_frame-")],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True, k = "-footer_frame-")]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path)
    window.bind("<Escape>", "-ESCAPE-")
    # 'ctrl + s' event
    window.bind("<Control-KeyPress-s>", "-ctrl_s-")
    window.bind("<Control-KeyPress-S>", "-ctrl_s-")

    window.Maximize()

    selected_item_id = False
    admin_mode = False

    while True:
        event, value = window.read(timeout = 1000)
        #print("event: ", end = "\t"); print(event)
        #print("value: ", end = "\t"); print(value)

        # Toggle admin mode
        if event in ["-ctrl_s-"]:
            text_to_log("-ctrl_s-")
            if not admin_mode:
                admin_mode = admin_main()
                if admin_mode:
                    text_to_log("ADMIN MODE ENABLED")
                    window["-QUICK_BACKUP-"].update(visible = True)
                    window["-DELETE_BACKUP-"].update(visible = True)
                    window["-hostname-"].update("RENDSZERGAZDA MÓD", background_color = "red", font = SMALL_BOLD)
            else:
                event = "-DISABLE_ADMIN-"

        # Disable admin mode
        if event in ["-DISABLE_ADMIN-"]:
            text_to_log("-DISABLE_ADMIN-")
            admin_mode = False
            window["-QUICK_BACKUP-"].update(visible = False)
            window["-DELETE_BACKUP-"].update(visible = False)
            window["-hostname-"].update(config_path.hostname, background_color = windows.gui_theme.BG_C, font = FOOTER_F)

        # Admin mode
        if event in ["-QUICK_BACKUP-"]:
            text_to_log("-QUICK_BACKUP-")
            backup_db()
            window["-header-"].update("SIKERES MENTÉS", background_color = "green")
        if event in ["-DELETE_BACKUP-"]:
            text_to_log("-DELETE_BACKUP-")
            funct.file_handle.clean_dir(config_path.temp_path)
            window["-header-"].update("MENTÉSEK TÖRÖLVE", background_color = "green")

        # Exit
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            if admin_mode:
                text_to_log("EXIT")
                return not admin_mode
        # Timeout event
        if event == "__TIMEOUT__":
            window["-time-"].update(get_time())
            if backup_countdown > 0:
                backup_countdown -= 1
            else:
                if not admin_mode:
                    backup_db()
                    backup_countdown = config_path.BP_INTERVAL_S

        # Checking for table click
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
                    text_to_log(value["-new_package-"] + " PACK NO. ADDED")
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
        if event == "-SETTINGS-":
            text_to_log("-SETTINGS-")
            settings_main(admin_mode)
            config_json = funct.json_handle.config_read()
            usercode = config_json["usercode"]

        # Upload
        elif event in ["-UPLOAD-"]:
            text_to_log("-UPLOAD-")
            succ_upload = upload_main()
            if succ_upload:
                if sgpop_yn("Törli a helyi adatokat?"):
                    text_to_log("DB DELETE")
                    window.close()
                    local_db.close()
                    funct.file_handle.clean_dir(os.path.join(config_path.path, config_path.DB_SUBPATH))
                    return True

    window.close()
    return False


if __name__ == "__main__":
    main_open = True
    while main_open:
        main_open = main()
