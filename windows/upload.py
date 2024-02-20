import PySimpleGUI as sg
import windows.gui_theme
import config_path

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - CSOMAGOLÁS \ FELTÖLTÉS"
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

def main():

    header_layout = [
        [sg.Push(), sg.Text(header, font = medium_bold), sg.Push()]
    ]

    options_layout = [
        [sg.Push(), sg.Text("Indulhat az adatok feltöltése?", font = medium_f), sg.Push()],
        [sg.Push(), sg.Button("IGEN", k = "-UPLOAD_YES-", font = small_f, button_color = "green", size = 10), sg.Push(), sg.Button("NEM", k = "-UPLOAD_NO-", font = small_f, button_color = "red", size = 10), sg.Push()]
    ]

    footer_layout = [
        [sg.Push(), sg.Text(config_path.version, font = footer_f), sg.Push(), sg.VerticalSeparator(), sg.Push(), sg.Text(config_path.hostname, font = footer_f), sg.Push()]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_bold, expand_x = True)],
        [sg.Frame("", options_layout, font = small_bold, expand_x = True)],
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
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-" or event == "-UPLOAD_NO-":
            window.close()
            break
        if event == "-UPLOAD_YES-":
            None