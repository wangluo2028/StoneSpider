#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HearthstoneLanguage
import HearthstoneApplication
from mss import mss
from pywinauto.application import Application
from airtest.core.api import *
#pip freeze > requirements.txt

if __name__ == "__main__":
    init_device("Windows")

    #Application(backend='uia').start('Battle.net Launcher.exe')
    hslang = HearthstoneLanguage.HearthstoneLang()
    hsApp = HearthstoneApplication.HearthstoneApplication(hslang)
    hsApp.autoSearchBattleNetPath()
    hsApp.autoConnectBattleNet()
    hsApp.autoSearchHearthStoneWindow()
    hsApp.mainLoop()
    #hsApp.testMove()