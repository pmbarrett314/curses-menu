#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import os  # curses is the interface for capturing key presses on the menuData, os launches the files
import platform
from enum import Enum


class menuItem(Enum):
    MENU = "menu"
    COMMAND = "command"
    EXITMENU = "exitmenu"
    FUNCTION = "function"
    FUNCTIONMENU = "functionmenu"
    NUMBER = "number"





# This function displays the appropriate menuData and returns the option selected
def displayMenu(screen, menu, parent):

    if parent is None:
        lastoption = "Exit"
    else:
        lastoption = "Return to %s menu" % parent['title']

    optioncount = len(menu['options'])  # how many options in this menuData




# This function calls showmenu and then acts on the selected item


def processMenu(screen, menu, functions, parent=None):
    optioncount = len(menu['options'])
    exitmenu = False

    getin = None

    while not exitmenu:  # Loop until the user exits the menuData
        getin = displayMenu(screen, menu, parent)
        if getin == optioncount:
            exitmenu = True
        elif menu['options'][getin]['type'] == menuItem.FUNCTION:
            curses.def_prog_mode()
            clear_screen()
            screen.clear()
            functions[menu['options'][getin]['function']]()
            screen.clear()  # clears previous screen on key press and updates display based on pos
            curses.reset_prog_mode()  # reset to 'current' curses environment
            curses.curs_set(1)  # reset doesn't do this right
            curses.curs_set(0)
        elif menu['options'][getin]['type'] == menuItem.COMMAND:
            curses.def_prog_mode()  # save curent curses environment
            clear_screen()
            screen.clear()  # clears previous screen
            os.system(menu['options'][getin]['command'])  # run the command
            screen.clear()  # clears previous screen on key press and updates display based on pos
            curses.reset_prog_mode()  # reset to 'current' curses environment
            curses.curs_set(1)  # reset doesn't do this right
            curses.curs_set(0)
        elif menu['options'][getin]['type'] == menuItem.MENU:
            screen.clear()  # clears previous screen on key press and updates display based on pos
            processMenu(screen, menu['options'][getin], functions, menu)  # display the submenu
            screen.clear()  # clears previous screen on key press and updates display based on pos
        elif menu['options'][getin]['type'] == menuItem.FUNCTIONMENU:
            curses.def_prog_mode()
            clear_screen()
            screen.clear()
            functions[menu['options'][getin]['function']]()
            screen.clear()  # clears previous screen on key press and updates display based on pos
            curses.reset_prog_mode()  # reset to 'current' curses environment
            curses.curs_set(1)  # reset doesn't do this right
            curses.curs_set(0)
            screen.clear()  # clears previous screen on key press and updates display based on pos
            processMenu(screen, menu['options'][getin], functions, menu)  # display the submenu
            screen.clear()  # clears previous screen on key press and updates display based on pos
        elif menu['options'][getin]['type'] == menuItem.EXITMENU or menu['options'][getin]['type'] == menuItem.NUMBER:
            exitmenu = True
    return getin


def runMenu(rootMenu, functions):



    # Main program
    number = processMenu(screen, rootMenu, functions)
    curses.endwin()  # VITAL! This closes out the menuData system and returns you to the bash prompt
    clear_screen()
    return number


def display_selection_menu(title, options):
    menu_data = {
        'title': title, 'type': menuItem.MENU, 'subtitle': "Please select an option...",
        'options': []
    }
    for item in options:
        menu_data["options"].append({'title': item, 'type': menuItem.NUMBER})
    return runMenu(menu_data, None)


def main():
    menu_data = {
        'title': "Program Launcher", 'type': menuItem.MENU, 'subtitle': "Please select an option...",
        'options': [
            {'title': "XBMC", 'type': menuItem.COMMAND, 'command': 'xbmc'},
            {'title': "Emulation Station - Hit F4 to return to menuData, Esc to exit game", 'type': menuItem.COMMAND,
             'command': 'emulationstation'},
            {'title': "Ur-Quan Masters", 'type': menuItem.COMMAND, 'command': 'uqm'},
            {'title': "Dosbox Games", 'type': menuItem.MENU, 'subtitle': "Please select an option...",
             'options': [
                 {'title': "Midnight Rescue", 'type': menuItem.COMMAND,
                  'command': 'dosbox /media/samba/Apps/dosbox/doswin/games/SSR/SSR.EXE -exit'},
                 {'title': "Outnumbered", 'type': menuItem.COMMAND,
                  'command': 'dosbox /media/samba/Apps/dosbox/doswin/games/SSO/SSO.EXE -exit'},
                 {'title': "Treasure Mountain", 'type': menuItem.COMMAND,
                  'command': 'dosbox /media/samba/Apps/dosbox/doswin/games/SST/SST.EXE -exit'},
             ]
             },
            {'title': "Pianobar", 'type': menuItem.COMMAND, 'command': 'clear && pianobar'},
            {'title': "Windows 3.1", 'type': menuItem.COMMAND,
             'command': 'dosbox /media/samba/Apps/dosbox/doswin/WINDOWS/WIN.COM -conf /home/pi/scripts/dosbox2.conf -exit'},
            {'title': "Reboot", 'type': menuItem.MENU, 'subtitle': "Select Yes to Reboot",
             'options': [
                 {'title': "NO", 'type': menuItem.EXITMENU, },
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
                 {'title': "YES", 'type': menuItem.COMMAND, 'command': 'sudo shutdown -r -time now'},
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
                 {'title': "", 'type': menuItem.COMMAND, 'command': ''},
             ]
             },

        ]
    }
    runMenu(menu_data, {})


if __name__ == "__main__":
    main()
