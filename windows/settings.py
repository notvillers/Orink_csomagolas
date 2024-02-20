import PySimpleGUI as sg
import windows.gui_theme
import config_path
import funct.json_handle

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

def sgpop(text):
    sg.popup_no_buttons(text, font = small_f, title = header)

def main():

    config_json = funct.json_handle.config_read()
    usercode = config_json["usercode"]

    header_layout = [
        [sg.Push(), sg.Text(header, font = medium_bold), sg.Push()]
    ]

    setting_layout = [
        [sg.Text("Felhasználó azonosító:", font = small_f), sg.Push(), sg.Input(usercode, k = "-usercode-", font = small_f, size = isize)]
    ]

    button_layout = [
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = small_f, size = bsize, bind_return_key = True), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.hostname, font = footer_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_bold, expand_x = True)],
        [sg.Frame("ADATOK", setting_layout, font = small_bold, expand_x = True)],
        [sg.Frame("OPCIÓK", button_layout, font = small_bold, expand_x = True)],
        [sg.VPush()],
        [sg.Frame("", footer_layout, font = small_bold, expand_x = True)]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze)
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    while True:
        event, value = window.read()
        print("event: ", end = "\t"); print(event)
        print("value: ", end = "\t"); print(value)
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-":
            window.close()
            break
        if event == "-UPDATE-":
            if value["-usercode-"]:
                funct.json_handle.config_update(usercode = value["-usercode-"])
                window.close()
                break
            else:
                sgpop("Üres azonosító nem rögzíthető!")