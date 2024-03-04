'''Admin window'''

import base64
import PySimpleGUI as sg
import windows.gui_theme
import config_path

# Theme
sg.theme_add_new("O8", windows.gui_theme.o8_theme)
sg.theme("O8")
HEADER = "ADMIN"
# Font
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

def main():
    '''Main definition, runs the GUI'''
    
    admin_layout = [
        [sg.VPush(background_color = "red")],
        [sg.Push(background_color = "red"), sg.Text("Jelszó:", font = MEDIUM_BOLD, background_color = "red"), sg.Push(background_color = "red")],
        [sg.Push(background_color = "red"), sg.Input("", k = "-admin_data-", font = SMALL_F, size = ISIZE, password_char = "*", background_color = "white"), sg.Push(background_color = "red")],
        [sg.Push(background_color = "red"), sg.Button("OK", k = "-OK-", font = SMALL_F, size = BSIZE, bind_return_key = True, mouseover_colors = "white"), sg.Push(background_color = "red")],
        [sg.Push(background_color = "red"), sg.Text("", k = "-info-", font = MEDIUM_BOLD, background_color = "red"), sg.Push(background_color = "red")],
        [sg.VPush(background_color = "red")]
    ]

    layout = [
        [sg.Frame("ADMIN", admin_layout, font = LARGE_BOLD, expand_x = True, expand_y = True, background_color = "red")]
    ]

    window = sg.Window(HEADER, layout, resizable = True, finalize = True, size = windows.gui_theme.main_sgisze, icon = config_path.icon_path, background_color = "red")
    window.bind("<Escape>", "-ESCAPE-")
    window.Maximize()

    passwd_encoded = "a29sYmFjZQ=="
    passwd = base64.b64decode(passwd_encoded).decode("utf-8")

    while True:
        event, value = window.read()
        #print("event:", end = "\t"); print(event)
        #print("value:", end = "\t"); print(value)
        if event in ["Exit", sg.WIN_CLOSED, "-ESCAPE-"]:
            window.Close()
            return False
        if event == "-OK-":
            if value["-admin_data-"] == passwd:
                window.Close()
                return True
            if not value["-admin_data-"]:
                window["-info-"].update("Üres jelszó!")
            else:
                window["-info-"].update("Hibás jelszó!")

    window.Close()
    return False
