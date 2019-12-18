#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui
import pygetwindow as gw
#from ctypes import *
import ctypes

class HearthstoneWindow:
    def __init__(self, hsLang):
        self._hsLang = hsLang
        self._hwndHearthstone = None

    @property
    def hsLang(self):
        return self._hsLang

    def autoSearchWindow(self):
        #self._hwndHearthstone = win32gui.FindWindow(None, self.hsLang.windowTitle)
        hearthstoneWindows = gw.getWindowsWithTitle(self.hsLang.windowTitle)
        self._hwndHearthstone = None
        for hsWindow in hearthstoneWindows:
            if hsWindow.title == self.hsLang.windowTitle:
                self._hwndHearthstone = hsWindow
                break

    def testMove(self):
        #windowSize = win32gui.GetWindowRect(self._hwndHearthstone)
        self._hwndHearthstone.activate()
        #https://stackoverflow.com/questions/34139450/getwindowrect-returns-a-size-including-invisible-borders
        #https://stackoverflow.com/questions/52308952/python-inactive-screen-capture
        self._hwndHearthstone.moveTo(0, 0)
        #windll.dwmapi.DwmGetWindowAttribute
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            f = None
        if f:  # Vista & 7 stuff
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self._hwndHearthstone._hWnd),
              ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
              ctypes.byref(rect),
              ctypes.sizeof(rect)
              )
            size = (rect.right - rect.left, rect.bottom - rect.top)
        else:
            size = self._hwndHearthstone.size
        testClientRect = win32gui.GetClientRect(self._hwndHearthstone._hWnd)
        print(self._hwndHearthstone.isMaximized)
        print(self._hwndHearthstone.isMinimized)
        #self._hwndHearthstone.maximize()
        #self._hwndHearthstone.minimize()