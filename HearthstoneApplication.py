#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import ctypes
from WindowUtil import WindowController
import numpy as np
import cv2
import subprocess
import win32.constants as win32Constant
from mss import mss
from PIL import Image
import winreg
import pywinauto
import pyautogui

class HearthstoneApplication:
    def __init__(self, hsLang):
        self._hsLang = hsLang

        self._hwndHearthstone = None
        self._hearthStonePath = None
        self._battleNetReg = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Battle.net"
        self._battleNetExe = r"\Battle.net Launcher.exe"
        self._battleNetPath = None
        self._application = pywinauto.Application(backend='uia')
        self._battleNetApplication = None
        self._battleNetWindow = None
        self._battleNetWinController = None
        self._hearthStoneWindow = None
        self._hearthStoneWinController = None

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

    @property
    def battleNetWindow(self):
        return self._battleNetWindow

    @property
    def battleNetHwnd(self):
        return self.battleNetWindow.wrapper_object().handle

    @property
    def battleNetWinController(self):
        return self._battleNetWinController

    @property
    def hearthStoneWindow(self):
        return self._hearthStoneWindow

    @property
    def hearthStoneHwnd(self):
        return self.hearthStoneWindow.wrapper_object().handle

    @property
    def hearthStoneWinController(self):
        return self._hearthStoneWinController

    def autoSearchBattleNetPath(self):
        if not self.battleNetPath:
            hbattleNetKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self._battleNetReg)
            self._battleNetPath = winreg.QueryValueEx(hbattleNetKey, "InstallLocation")[0] + self._battleNetExe
            winreg.CloseKey(hbattleNetKey)

    def autoConnectBattleNet(self):
        self.autoSearchBattleNetPath()
        #os.startfile(self.battleNetPath)
        try:
            self.application.connect(path=self.battleNetPath)
        except Exception as e:
            subprocess.Popen(self.battleNetPath,
                             shell=True,
                             creationflags=win32Constant.DETACHED_PROCESS|win32Constant.CREATE_NEW_PROCESS_GROUP,
                             cwd=os.path.dirname(self.battleNetPath))

    def autoSearchBattleNetSystemTrayOnHiddenTray(self):
        pass

    def autoSearchBattleNetSystemTrayOnTaskbar(self):
        self.application.connect(path="explorer.exe")
        systemTrayWindow = self.application.window(class_name="Shell_TrayWnd")

        bSystemTrayOnTaskbarConnected = False
        for battleNetLang, battleNetWindowTitle in self.hsLang.battleNetWindowTitles.items():
            try:
                battleNetButtonOnTaskbar = systemTrayWindow.child_window(title_re=battleNetWindowTitle)
                battleNetButtonOnTaskbar.click()
                bSystemTrayOnTaskbarConnected = True
            except Exception as e:
                pass
            if bSystemTrayOnTaskbarConnected:
                break

        if not bSystemTrayOnTaskbarConnected:
            self.application.connect(path="explorer.exe")
            systemTrayWindow = self.application.window(class_name="Shell_TrayWnd")
            SystemTrayUpWindow = systemTrayWindow.child_window(title="Notification Chevron").wrapper_object()
            SystemTrayUpWindow.click()
            #time.sleep(0.25)
            systemTrayOverflowApplication = self.application.connect(class_name="NotifyIconOverflowWindow")
            systemTrayOverflowWindow = self.application.window(class_name="NotifyIconOverflowWindow")
            systemTrayOverflowWindow.wait('visible', timeout=30, retry_interval=3)
            # ddm = desk.create_window(best_match="DropDownMenu")
            # desk.wait_for_window_to_appear(ddm, wait_for='ready', timeout=20, retry_interval=2)
            # ddm.child_window(title= < select option >, control_type = "MenuItem").click_input()
            bSystemTrayOnHiddenTaskbarConnected = False
            for battleNetLang, battleNetWindowTitle in self.hsLang.battleNetWindowTitles.items():
                try:
                    battleNetButtonOnHiddenTaskbar = systemTrayOverflowWindow.child_window(title_re=battleNetWindowTitle)
                    battleNetButtonOnHiddenTaskbar.click()
                    bSystemTrayOnHiddenTaskbarConnected = True
                except Exception as e:
                    pass
                if bSystemTrayOnHiddenTaskbarConnected:
                    break
            if not bSystemTrayOnHiddenTaskbarConnected:
                self.autoConnectBattleNet()


    def autoSearchBattleNetWindow(self):
        bBattleNetWindowConnected = False
        for battleNetLang, battleNetWindowTitle in self.hsLang.battleNetWindowTitles.items():
            try:
                self._battleNetWinController = WindowController(title=battleNetWindowTitle)
                self.application.connect(handle=self._battleNetWinController.hwnd)
                self._battleNetWindow = self.application.window(handle=self._battleNetWinController.hwnd)
                #self._battleNetWinController = WindowController(handle=self.battleNetHwnd)
                #self._battleNetWinController.bringToFront()
                #self._battleNetWindow.print_control_identifiers()
                #TODO: play hearth stone
                self._battleNetWinController.takeScreenshot()
                self._battleNetWinController.clickButtonImage('Resources/App/battleNet_EnterGame.png')
                self.hsLang.battleNetLang = battleNetLang
                bBattleNetWindowConnected = True
            except Exception as e:
                print('error message' + str(e))
            if bBattleNetWindowConnected:
                break

        if not bBattleNetWindowConnected:
            #self.autoSearchBattleNetSystemTrayOnTaskbar()
            self.autoConnectBattleNet()

    def autoSearchHearthStoneWindow(self):
        bHearthWindowConnected = False
        for hsLanguage, hsWindowTitle in self.hsLang.hsWindowTitles.items():
            try:
                self._hearthStoneWinController = WindowController(title=hsWindowTitle)
                self.application.connect(handle=self._hearthStoneWinController.hwnd)
                self._hearthStoneWindow = self.application.window(handle=self._hearthStoneWinController.hwnd)
                # self.application.connect(title=hsWindowTitle, visible_only=False, top_level_only=True)
                # self._hearthStoneWindow = self.application.window(title=hsWindowTitle,
                #                                                   visible_only=False, top_level_only=True)
                #self._hearthStoneWinController = WindowController(handle=self.hearthStoneHwnd)
                self._hearthStoneWinController.bringToFront()
                self.hsLang.hsLang = hsLanguage
                bHearthWindowConnected = True
            except Exception as e:
                pass
            if bHearthWindowConnected:
                break

        if not bHearthWindowConnected:
            self.autoSearchBattleNetWindow()

    def mainLoop(self):
        while True:
            print('main loop')
            try:
                if not self.hearthStoneWinController:
                    raise Exception("Heart window invalid")
                screenShot = self.hearthStoneWinController.takeScreenshot()
                self.analyzeScreenShot(screenShot)
            except Exception as e:
                self.autoSearchHearthStoneWindow()
            # if (cv2.waitKey(1) & 0xFF) == ord('q'):
            #     cv2.destroyAllWindows()
            #     break

    def analyzeScreenShot(self, screenShot):
        self.hearthStoneWindow.print_control_identifiers()
        #cv2.imshow('test', np.array(screenShot))

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