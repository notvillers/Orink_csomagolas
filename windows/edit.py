import PySimpleGUI as sg
import windows.gui_theme
import config_path

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - CSOMAGOLÁS \ MÓDOSÍTÁS"
# Font
footer_bold = windows.gui_theme.font_arial_footer_bold
footer_f = windows.gui_theme.font_arial_footer
small_f = windows.gui_theme.font_arial_kicsi
small_bold = windows.gui_theme.font_arial_kicsi_bold
medium_f = windows.gui_theme.font_arial_kozepes
medium_bold = windows.gui_theme.font_arial_kozepes_bold
large_f = windows.gui_theme.font_arial_nagy
large_bold = windows.gui_theme.font_arial_nagy_bold

def sgpop(text):
    sg.popup_no_buttons(text, font = small_f, title = header)

def main(selected_item):

    package_id = selected_item[0]
    package_no = selected_item[1]
    package_user = selected_item[2]

    header_layout = [
        [sg.Push(), sg.Text(header, font = medium_bold), sg.Push()]
    ]

    package_layout = [
        [sg.Text("ID: ", font = small_f), sg.Push(), sg.Input(package_id, font = small_f, size = 20, readonly = True, disabled_readonly_background_color = windows.gui_theme.bg_c)],
        [sg.Text("Csomagszám: ", font = small_f), sg.Push(), sg.Input(package_no, k = "-package_no-", font = small_f, size = 20)],
        [sg.Text("Rögzítő: ", font = small_f), sg.Push(), sg.Input(package_user, font = small_f, size = 20, readonly = True, disabled_readonly_background_color = windows.gui_theme.bg_c)]
    ]

    button_layout = [
        [sg.Push(), sg.Button("FRISSÍTÉS", k = "-UPDATE-", font = small_f, size = 10, bind_return_key = True), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.version, font = footer_f), sg.Push(), sg.VerticalSeparator(), sg.Push(), sg.Text(config_path.hostname, font = footer_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_f, expand_x = True)],
        [sg.Frame("CSOMAG", package_layout, font = small_bold, expand_x = True)],
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
            return None
        if event == "-UPDATE-":
            if value["-package_no-"]:
                window.close()
                return [package_id, value["-package_no-"], package_user]
            else:
                sgpop("Üres csomagszám nem rögzítehető!")