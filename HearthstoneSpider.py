#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HearthstoneLanguage
import HearthstoneApplication
from mss import mss
from pywinauto.application import Application

#pip freeze > requirements.txt

if __name__ == "__main__":
    #Application(backend='uia').start('Battle.net Launcher.exe')
    language = HearthstoneLanguage.Language.English
    hslang = HearthstoneLanguage.HearthstoneLang(language)
    hsApp = HearthstoneApplication.HearthstoneApplication(hslang)
    hsApp.autoSearchBattleNetPath()
    hsApp.autoConnectBattleNet()
    hsApp.autoSearchWindow()
    hsApp.mainLoop()
    #hsApp.testMove()