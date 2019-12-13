#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui
import pygetwindow as gw

class HearthstoneWindow:
    def __init__(self, hsLang):
        self._hsLang = hsLang
        self._hwndHearthstone = None

    @property
    def hsLang(self):
        return self._hsLang

    def autoSearchWindow(self):
        #self._hwndHearthstone = win32gui.FindWindow(None, self.hsLang.windowTitle)
        self._hwndHearthstone = gw.getWindowsWithTitle(self.hsLang.windowTitle)[0]

    def testMaximize(self):
        #windowSize = win32gui.GetWindowRect(self._hwndHearthstone)
        print(self._hwndHearthstone.isMaximized)
        print(self._hwndHearthstone.isMinimized)
        self._hwndHearthstone.maximize()
        self._hwndHearthstone.minimize()