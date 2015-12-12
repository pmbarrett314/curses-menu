#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Topmenu and the submenus are based of the example found at this location http://blog.skeltonnetworks.com/2010/03/python-curses-custom-menuData/
# The rest of the work was done by Matthew Bennett and he requests you keep these two mentions when you reuse the code :-)
# Basic code refactoring by Andrew Scheller


# This file from: https://gist.github.com/abishur/2482046
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


def clear_screen():
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('reset')


# This function displays the appropriate menuData and returns the option selected
def displayMenu(screen, menu, parent):
    h = curses.color_pair(1)  # h is the coloring for a highlighted menuData option
    n = curses.A_NORMAL  # n is the coloring for a non highlighted menuData option
    curses.init_pair(1, curses.COLOR_BLACK,
                     curses.COLOR_WHITE)  # Sets up color pair #1, it does black text with white background
    # work out what text to display as the last menuData option
    if parent is None:
        lastoption = "Exit"
    else:
        lastoption = "Return to %s menu" % parent['title']

    optioncount = len(menu['options'])  # how many options in this menuData

    pos = 0  # pos is the zero-based index of the hightlighted menuData option. Every time runmenu is called, position returns to 0, when runmenu ends the position is returned and tells the program what opt$
    oldpos = None  # used to prevent the screen being redrawn every time
    x = None  # control for while loop, let's you scroll through options until return key is pressed then returns pos to program

    # Loop until return key is pressed
    while x != ord('\n'):
        if pos != oldpos:
            oldpos = pos
            screen.border(0)
            screen.addstr(2, 2, menu['title'], curses.A_STANDOUT)  # # Title for this menuData
            screen.addstr(4, 2, menu['subtitle'], curses.A_BOLD)  # # Subtitle for this menuData

            # Display all the menuData items, showing the 'pos' item highlighted
            for index in range(optioncount):
                textstyle = n
                if pos == index:
                    textstyle = h
                screen.addstr(5 + index, 4, "%d - %s" % (index + 1, menu['options'][index]['title']), textstyle)
            # Now display Exit/Return at bottom of menuData
            textstyle = n
            if pos == optioncount:
                textstyle = h
            screen.addstr(5 + optioncount, 4, "%d - %s" % (optioncount + 1, lastoption), textstyle)
            screen.refresh()
            # finished updating screen

        x = screen.getch()  # Gets user input

        # What is user input?
        if x >= ord('1') and x <= ord(str(optioncount + 1)):
            pos = x - ord('0') - 1  # convert keypress back to a number, then subtract 1 to get index
        elif x == 258:  # down arrow
            if pos < optioncount:
                pos += 1
            else:
                pos = 0
        elif x == 259:  # up arrow
            if pos > 0:
                pos += -1
            else:
                pos = optioncount

    # return index of the selected item
    return pos


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
    screen = curses.initscr()  # initializes a new window for capturing key presses
    curses.noecho()  # Disables automatic echoing of key presses (prevents program from input each key twice) @UndefinedVariable
    curses.cbreak()  # Disables line buffering (runs each key as it is pressed rather than waiting for the return key to pressed) @UndefinedVariable
    curses.start_color()  # Lets you use colors when highlighting selected menuData option
    screen.keypad(1)  # Capture input from keypad

    # Main program
    number = processMenu(screen, rootMenu, functions)
    curses.endwin()  # VITAL! This closes out the menuData system and returns you to the bash prompt. @UndefinedVariable
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
