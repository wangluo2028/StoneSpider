#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygetwindow as gw
import ctypes
from WindowUtil import WindowController
import numpy as np
import cv2
import subprocess
from mss import mss
from PIL import Image
import winreg
import pywinauto

class HearthstoneApplication:
    def __init__(self, hsLang):
        self._hsLang = hsLang
        self._hearthWinController = None
        self._hwndHearthstone = None
        self._hearthStonePath = None
        self._battleNetReg = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Battle.net"
        self._battleNetPath = r"\Battle.net.exe"
        self._application = pywinauto.Application(backend='uia')
        self._battleNetApplication = None
        self._battleNetWindow = None

    @property
    def hsLang(self):
        return self._hsLang

    @property
    def battleNetPath(self):
        return self._battleNetPath

    @property
    def application(self):
        return self._application

    @property
    def battleNetApplication(self):
        return self._battleNetApplication

    def autoSearchBattleNetPath(self):
        hbattleNetKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self._battleNetReg)
        self._battleNetPath = winreg.QueryValueEx(hbattleNetKey, "InstallLocation")[0] + self._battleNetPath
        winreg.CloseKey(hbattleNetKey)

    def autoConnectBattleNet(self):
        try:
            self._battleNetApplication = self.application.connect(title_re = self.hsLang.battleNetWindowTitle)
        except pywinauto.application.ProcessNotFoundError:
            try:
                self._battleNetApplication = self.application.start(self.battleNetPath, 5)
            except Exception:
                print('Please install battle net and hearthstone')
                self._battleNetApplication = None

        self._battleNetWindow = self._battleNetApplication.top_window()
        self._test = self._battleNetWindow.print_control_identifiers()
        print('test')

    def autoConnectHearthStone(self):
        pass

    def autoSearchWindow(self):
        try:
            self._hearthWinController = WindowController(self.hsLang.hsWindowTitle)
        except Exception:
            subprocess.call(self._hearthStonePath)
        #self._hwndHearthstone = win32gui.FindWindow(None, self.hsLang.windowTitle)
        # hearthstoneWindows = gw.getWindowsWithTitle(self.hsLang.windowTitle)
        # self._hwndHearthstone = None
        # for hsWindow in hearthstoneWindows:
        #     if hsWindow.title == self.hsLang.windowTitle:
        #         self._hwndHearthstone = hsWindow
        #         break

    def mainLoop(self):
        while True:
            screenShot = self._hearthWinController.takeScreenshot()
            self.analyzeScreenShot(screenShot)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

    def analyzeScreenShot(self, screenShot):
        cv2.imshow('test', np.array(screenShot))




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
        print(size)
        print(testClientRect)
        print(self._hwndHearthstone.isMaximized)
        print(self._hwndHearthstone.isMinimized)
        #self._hwndHearthstone.maximize()
        #self._hwndHearthstone.minimize()