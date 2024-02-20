import PySimpleGUI as sg
import windows.gui_theme
from funct.log import text_to_log
import os
import sys
import config_path
import funct.json_handle
from funct.sqlite_handle import connection as sqlite_connection
from funct.db_config import csomag_table_create, csomag_table_select, csomag_table_insert, csomag_table_delete

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - ORINK: CSOMAGOLÁS"
# Font
footer_f = windows.gui_theme.font_arial_footer
small_f = windows.gui_theme.font_arial_kicsi
small_bold = windows.gui_theme.font_arial_kicsi_bold
medium_f = windows.gui_theme.font_arial_kozepes
medium_bold = windows.gui_theme.font_arial_kozepes_bold
large_f = windows.gui_theme.font_arial_nagy
large_bold = windows.gui_theme.font_arial_nagy_bold

def sgpop(text):
    sg.popup_no_buttons(text, font = small_f, title = header)

def main():
    text_to_log(header + " started")    

    if funct.json_handle.create_config():
        text_to_log("please fill out the json in " + config_path.config_json_path)
        sys.exit()
    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]
    hostname = config_path.hostname

    local_db = sqlite_connection()
    local_db.execute(csomag_table_create)
    columns, results = local_db.select(csomag_table_select)

    header_layout = [
        [sg.Push(), sg.Text(header, font = large_bold), sg.Push()]
    ]

    option_layout = [
        [
            sg.Input("", k = "-new_package-", font = medium_f, size = 30), 
            sg.Button("Hozzáad", k = "-ADD-", font = medium_f, size = 12, bind_return_key = True),
            sg.Button("Módosít", k = "-EDIT-", font = medium_f, size = 12),
            sg.Button("Töröl", k = "-DELETE-", font = medium_f, size = 12, mouseover_colors = "red"),
            sg.Push(), sg.Text("", k = "-info-", font = medium_bold, text_color = "red"), sg.Push()
        ]
    ]

    packages_layout = [
        [
            sg.Table(
                values = results, 
                headings = columns, 
                key = "-packages-", 
                font = medium_f,
                justification = 'right',
                auto_size_columns = True, 
                enable_events = True, 
                enable_click_events = True, 
                expand_x = True, 
                expand_y = True,
                header_text_color = windows.gui_theme.bg_c,
                header_background_color = windows.gui_theme.txt_c,
                sbar_background_color = windows.gui_theme.txt_c,
                sbar_frame_color = windows.gui_theme.bg_c,
                sbar_trough_color = windows.gui_theme.bg_c,
                vertical_scroll_only = False,
                alternating_row_color = windows.gui_theme.ok_color
            )
        ]
    ]

    settings_layout = [
        [sg.Push(), sg.Button("Feltöltés", k = "-UPLOAD-", font = medium_f, size = 12), sg.Push(), sg.Button("Adatok", k = "-SETTINGS-", font = medium_f, size = 12), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.version, font = small_f), sg.Push(), sg.VerticalSeparator(), sg.Push(), sg.Text(config_path.hostname, font = small_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_bold, expand_x = True)],
        [sg.Frame("RÖGZÍTÉS", option_layout, font = small_bold, expand_x = True)],
        [sg.Frame("CSOMAGOK", packages_layout, font = small_bold, expand_x = True, expand_y = True)],
        [sg.VPush()],
        [sg.Frame("BEÁLLÍTÁSOK", settings_layout, font = small_bold, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = small_bold, expand_x = True)]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, location = (0, 0))
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    selected_item_id = False

    while True:
        event, value = window.read()
        print("event: ", end = "\t"); print(event)
        print("value: ", end = "\t"); print(value)
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-":
            break
        if event[0] == "-packages-" and event[1] == "+CLICKED+" and event[2][0] not in (None, -1) and event[2][1] not in (None, -1):
            selected_item = results[event[2][0]]
            selected_item_id = selected_item[0]
            print(selected_item)
            print(selected_item_id)
        if event == "-ADD-":
            if value["-new_package-"]:
                if not local_db.is_value_there(columns, results, "Csomagszám", value["-new_package-"]):
                    window["-info-"].update("")
                    local_db.insert(csomag_table_insert, (value["-new_package-"], usercode, hostname))
                    columns, results = local_db.select(csomag_table_select)
                    window["-new_package-"].update("")
                    window["-packages-"].update(values = results)
                else:
                    window["-info-"].update("Ismétlődés!")
                    window["-new_package-"].update("")
            else:
                window["-info-"].update("Üres csomagszám!")
        if event == "-EDIT-":
            if selected_item_id:
                from windows.edit import main as edit_main
                edit_main()
        if event == "-DELETE-":
            local_db.execute(csomag_table_delete, selected_item_id)
            columns, results = local_db.select(csomag_table_select)
            window["-packages-"].update(values = results)
        elif event in ["-UPLOAD-", "-SETTINGS-"]:
            sgpop( event + " fejlesztés alatt")

    window.close()
    os._exit(1)

if __name__ == "__main__":
    main()