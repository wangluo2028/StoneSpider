#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HearthstoneLanguage
import HearthstoneWindow
from mss import mss

#pip freeze > requirements.txt

if __name__ == "__main__":
    language = HearthstoneLanguage.Language.English
    hslang = HearthstoneLanguage.HearthstoneLang(language)
    hsWindow = HearthstoneWindow.HearthstoneWindow(hslang)
    hsWindow.autoSearchWindow()
    hsWindow.mainLoop()
    #hsWindow.testMove()