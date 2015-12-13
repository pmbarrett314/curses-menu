
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


