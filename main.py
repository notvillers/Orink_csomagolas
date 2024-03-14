#!/usr/bin/env python3
'''Main'''

import os
import base64
import PySimpleGUI as sg
import windows.gui_theme
from funct.log import text_to_log
from funct.slave import get_datetime
import config_path
import funct.json_handle
import funct.file_handle
import funct.slave
import funct.ftp_handle
from funct.sqlite_handle import Connection as sqlite_connection
from funct.db_config import CSOMAG_TABLE_CREATE, CSOMAG_TABLE_SELECT, CSOMAG_TABLE_INSERT, CSOMAG_TABLE_DELETE, CSOMAG_TABLE_UPDATE_BY_ID
from windows.edit import main as edit_main
from windows.settings import main as settings_main
from windows.upload import main as upload_main
from windows.admin import main as admin_main
from windows.event_viewer import main as event_main
from windows.popup import pop_esc_yn

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "OCTOPY - CSOMAGOLÁS"
# Set process title
if config_path.IS_MACOS:
    import setproctitle
    setproctitle.setproctitle(HEADER)
    setproctitle.setthreadtitle(HEADER)
SGSIZE = windows.gui_theme.main_sgisze
ICON_PATH = config_path.icon_path if not config_path.IS_MACOS else base64.b64encode(open(os.path.join(config_path.icon_macos_path), "rb").read())
ICON_IN_PATH = config_path.icon_in_path
INFO_PATH = config_path.info_path
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
BP_INTERVAL_M = config_path.BP_INTERVAL_M

# Variable(s)
EXIT_TRY_WITHOUT_ADMIN = 0
IS_LINUX = config_path.IS_LINUX
IS_MACOS = config_path.IS_MACOS
EVENT_KEYS = config_path.EVENT_KEYS

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


def del_db(connection):
    '''closes connection and deletes db'''

    connection.close()
    funct.file_handle.clean_dir(os.path.join(config_path.path, config_path.DB_SUBPATH))


def shortcut_info():
    '''return shortcut info list'''
    info = []
    for event_key in EVENT_KEYS:
        if event_key["info"] not in info and event_key["info"] is not None:
            info.append(event_key["info"])
    info_txt = "\n".join(info)
    return info_txt


def download_users():
    '''Downloads users.csv from ftp server'''

    ftp_json = funct.json_handle.ftp_read()
    if funct.slave.ping_srvr(ftp_json["hostname"], 5):
        text_to_log(ftp_json["hostname"] + " is up")
        ftp_client = funct.ftp_handle.Client(
            hostname = ftp_json["hostname"],
            username = ftp_json["username"],
            password = ftp_json["password"]
        )
        ftp_client.download(config_path.FTP_USERS_SUBPATH, config_path.SRC_PATH, "users.csv")
    else:
        text_to_log(ftp_json["hostname"] + " is down")


def main(admin_mode = False):
    '''Main definition, runs the GUI'''

    text_to_log(HEADER + " started")

    # Check for json files
    json_text = ""
    if funct.json_handle.create_config():
        json_text += "Kérlek töltsd ki a felhasználó adatokat!\n"

    if funct.json_handle.create_ftp():
        json_text += "Kérlek töltsd ki az FTP adatokat!"
    else:
        download_users()

    if json_text:
        pop_esc_yn(text = json_text)


    # Configs
    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]
    hostname = config_path.hostname

    # DB
    local_db = sqlite_connection()
    local_db.execute(CSOMAG_TABLE_CREATE)
    columns, results = local_db.select(CSOMAG_TABLE_SELECT)

    # Backup countdown
    backup_countdown = BP_INTERVAL_M

    # Menu
    menu_def = [["&Fájl", ["!&Importálás::-import-", "!&Exportálás::-export-"]], ["&Rendszergazda", ["!&Eseménynapló::-event_view-", "---", "!&Mentés::-backup-", "---", "!&Tábla ürítése::-table_clear-", "!&Demo betöltése::-demo_load-", "---", "!&Kilépés::-ESCAPE-"]]]
    menu_def_admin = [["&Fájl", ["!&Importálás::-import-", "!&Exportálás::-export-"]], ["&Rendszergazda", ["&Eseménynapló::-event_view-", "---", "&Mentés::-backup-", "---", "&Tábla ürítése::-table_clear-", "&Demo betöltése::-demo_load-", "---", "&Kilépés::-ESCAPE-"]]]

    # Option layout
    option_layout = [
        [
            sg.Input("", k = "-new_package-", font = SMALL_F),
            sg.Button("HOZZÁADÁS", k = "-ADD-", font = SMALL_F, bind_return_key = True, button_color = "green"),
            sg.Button("MÓDOSÍTÁS", k = "-EDIT-", font = SMALL_F),
            sg.Button("TÖRLÉS", k = "-DELETE-", font = SMALL_F, button_color = "red"),
            sg.Push(), sg.Text("", k = "-info-", font = MEDIUM_BOLD, text_color = "red"), sg.Push(),
            place(sg.Button("TEMP MENT", k = "-QUICK_BACKUP-", font = SMALL_F, button_color = "green", visible = False)),
            place(sg.Button("TEMP TÖRÖL", k = "-DELETE_BACKUP-", font = SMALL_F, button_color = "red", visible = False)),
        ]
    ]

    # Packages layout
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

    # Settings layout
    settings_layout = [
        [
            sg.Push(), sg.Button("ADATOK", k = "-SETTINGS-", font = SMALL_F),
            sg.Push(), sg.Button("FELTÖLTÉS", k = "-UPLOAD-", font = SMALL_F), sg.Push(),
        ]
    ]

    # Footer layout
    footer_layout = [
        [sg.Text(HOSTNAME, k = "-hostname-", font = FOOTER_F), sg.Push(), sg.Button("", k = "-INFO-", image_filename = INFO_PATH)]
    ]

    menu_layout = [[sg.Menu(menu_def, font = FOOTER_F, k = "-menu-")]]

    # Layout
    layout = [
        [sg.Frame("RÖGZÍTÉS", option_layout, font = SMALL_BOLD, expand_x = True, k = "-option_frame-")],
        [sg.Frame("CSOMAGOK", packages_layout, font = SMALL_BOLD, expand_x = True, expand_y = True, k = "-packages_frame-")],
        [sg.Frame("BEÁLLÍTÁSOK", settings_layout, font = SMALL_BOLD, expand_x = True, k = "-settings_frame-")],
        [sg.Frame("", footer_layout, font = SMALL_BOLD, expand_x = True, k = "-footer_frame-")],
        [sg.Push(), sg.Image(ICON_IN_PATH, k = "-icon-"), sg.Push()]
    ]

    final_layout = ((menu_layout + layout) if not IS_LINUX else layout)

    # Window
    window = sg.Window(HEADER, final_layout, resizable = True, finalize = True, size = SGSIZE, location = (0, 0), icon = ICON_PATH)

    # Events
    # Bind events
    for event_key in EVENT_KEYS:
        for key in event_key["key"]:
            window.bind(key, event_key["event"])

    # Maximize
    window.Maximize()

    # ctrl event
    ctrl_event = False

  # Selected items ID
    selected_item_id = False

    # Run
    while True:
        # Changing to admin mode, if necessary
        if admin_mode:
            text_to_log("ADMIN MODE ENABLED")
            window["-QUICK_BACKUP-"].update(visible = True)
            window["-DELETE_BACKUP-"].update(visible = True)
            if not IS_LINUX:
                window["-menu-"].update(menu_def_admin)
            if not ctrl_event:
                window["-hostname-"].update("RENDSZERGAZDA MÓD", background_color = "red", font = SMALL_BOLD)
            else:
                window["-hostname-"].update("KIKAPCSOLÁSA: CTRL+S | GYORSGOMBOK: CTRL+I", background_color = "red", font = SMALL_BOLD)

        event, value = window.read(timeout = 60000)
        print("event: ", end = "\t"); print(event)
        print("value: ", end = "\t"); print(value)

        # ctrl event
        if event == "-ctrl-" and IS_MACOS:
            if not ctrl_event:
                window["-SETTINGS-"].update("CTRL + A")
                window["-UPLOAD-"].update("CTRL + F")
                ctrl_event = not ctrl_event
                if admin_mode:
                    window["-hostname-"].update("KIKAPCSOLÁSA: CTRL+S | ESEMÉNYNAPLÓ: CTRL+E")
            else:
                window["-SETTINGS-"].update("ADATOK")
                window["-UPLOAD-"].update("FELTÖLTÉS")
                if admin_mode:
                    window["-hostname-"].update("RENDSZERGAZDA MÓD")
                ctrl_event = not ctrl_event

        # Shortcut events:
        if event in ["-ctrl_i-", "-INFO-"]:
            pop_esc_yn(header = "Gyorsgombok",text = shortcut_info(), buttons = [])

        # Toggle admin mode
        if event == "-ctrl_s-":
            text_to_log("-ctrl_s-")
            if not admin_mode:
                admin_mode = admin_main()
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
            window["-info-"].update("Sikeres mentés!", text_color = "green")
        if event == "-DELETE_BACKUP-":
            text_to_log("-DELETE_BACKUP-")
            funct.file_handle.clean_dir(config_path.temp_path)
            window["-info-"].update("Mentések törölve!", text_color = "green")

        # Exit
        if event in ["Exit", "-ESCAPE-", sg.WIN_CLOSED] or "::-ESCAPE-" in event:
            global EXIT_TRY_WITHOUT_ADMIN
            if EXIT_TRY_WITHOUT_ADMIN > 4:
                pop_esc_yn(text = "Kérlek ne zárj be!")
                EXIT_TRY_WITHOUT_ADMIN = 0
            if admin_mode:
                text_to_log("EXIT")
                window.Close()
                return False, True
            if not admin_mode:
                EXIT_TRY_WITHOUT_ADMIN += 1
                text_to_log("TRYING TO EXIT WITHOUT ADMIN_MODE " + str(EXIT_TRY_WITHOUT_ADMIN))
            if event == sg.WIN_CLOSED:
                window.Close()
                return True, False

        # Restart
        if event == "-ctrl_r-" and admin_mode:
            return True, True

        # Timeout event
        if event == "__TIMEOUT__":
            if backup_countdown > 0:
                backup_countdown -= 1
            else:
                if not admin_mode:
                    backup_db()
                    backup_countdown = BP_INTERVAL_M

        # Checking for table click
        if event is not None:
            if event[0] == "-packages-" and event[1] == "+CLICKED+" and event[2][0] not in (None, -1) and event[2][1] not in (None, -1):
                selected_item = results[event[2][0]]
                selected_item_id = selected_item[0]

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
                    window["-info-"].update("Ismétlődés!", text_color = "red")
                    window["-new_package-"].update("")
            else:
                window["-info-"].update("Üres csomagszám!", text_color = "red")

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
                        window["-info-"].update("Ismétlődés!", text_color = "red")

        # Delete
        if event == "-DELETE-" and selected_item_id:
            if pop_esc_yn(text = "Biztosan törli?", buttons = ["IGEN", "NEM"]) == "-IGEN-":
                local_db.execute(CSOMAG_TABLE_DELETE, (selected_item_id))
                columns, results = local_db.select(CSOMAG_TABLE_SELECT)
                text_to_log("ID: " + str(selected_item_id) + " DELETED")
                window["-packages-"].update(values = results)
                window["-info-"].update("Csomag törölve!", text_color = "red")

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
            if succ_upload: #TODO: tiltva üres visszatöltés miatt
                if pop_esc_yn(text = "Törli a helyi adatokat?", buttons = ["IGEN", "NEM"]) == "-IGEN-":
                    text_to_log("DB DELETE")
                    window.close()
                    del_db(local_db)
                    if admin_mode:
                        return True, True
                    return True, False
                
        # Event viewer
        if event == "-ctrl_e-" and admin_mode:
            event_main()

        # Menu handling
        if "::" in event:
            # Import
            if "::-import-" in event:
                pass
            # Export
            if "::-export-" in event:
                pass

            # Admin mode
            if admin_mode:
                # Event view
                if "::-event_view-" in event:
                    event_main()
                # Load demo data
                if "::-demo_load-" in event:
                    if results:
                        window["-info-"].update("Már vannak adatok!")
                    else:
                        if pop_esc_yn(buttons = ["IGEN", "NEM"]) == "-IGEN-":
                            random_strings = funct.slave.generate_random_string_list(length = 100, string_length = 50)
                            for random_string in random_strings:
                                local_db.insert(CSOMAG_TABLE_INSERT, (random_string, usercode, hostname))
                                columns, results = local_db.select(CSOMAG_TABLE_SELECT)
                                window["-packages-"].update(values = results)
                                window["-info-"].update("Demo betöltve!", text_color = "green")
                # Clear table
                if "::-table_clear-" in event:
                    if pop_esc_yn(buttons = ["IGEN", "NEM"]) == "-IGEN-":
                        window.Close()
                        del_db(local_db)
                        return True, True
                if "::-backup-" in event:
                    backup_db()
                    window["-info-"].update("Sikeres mentés!", text_color = "green")

    window.close()
    return False, False


if __name__ == "__main__":
    MAIN_OPEN = True
    IS_ADMIN = False
    while MAIN_OPEN:
        if not IS_ADMIN:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = False)
        else:
            MAIN_OPEN, IS_ADMIN = main(admin_mode = True)
