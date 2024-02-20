import PySimpleGUI as sg
import windows.gui_theme

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
header = "OCTOPY - ORINK: CSOMAGOLÁS \ MÓDOSÍTÁS"
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

def main(id: int = None):
    
    header_layout = [
        [sg.Push(), sg.Text(header, font = large_bold), sg.Push()]
    ]

    package_layout = [
        [sg.Text("Package no.:", font = medium_f), sg.Input("testpackagenumber", k = "-package_no-", font = medium_f, size = 30)]
    ]

    layout = [
        [sg.Frame("", header_layout, font = small_f, expand_x = True)],
        [sg.Frame("CSOMAG", package_layout, font = small_f, expand_x = True)]
    ]

    window = sg.Window(header, layout, resizable = True, finalize = True)
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, value = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED or event == "-ESCAPE-":
            break

    window.close()